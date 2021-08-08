# pylint: disable=no-self-use,redefined-outer-name

import json
import os
import shutil
import tempfile
from typing import Callable, Dict, Iterator, List, NamedTuple
from unittest import mock

from _pytest.capture import CaptureFixture
from _pytest.fixtures import SubRequest
import pytest
from pytest_mock.plugin import MockerFixture

from funky import commands, errors


class Args(NamedTuple):
    args: List[str]
    color: bool


@pytest.fixture(autouse=True)
def cleandir() -> Iterator[None]:
    """Run tests in an empty directory."""
    newpath = tempfile.mkdtemp()
    os.chdir(newpath)
    yield
    shutil.rmtree(newpath)


#####################################################################
#  Tests                                                            #
#####################################################################
class Test_Add_and_Edit:
    """Tests for the Add and Edit commands."""

    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture) -> None:
        mocker.patch("funky.commands.sp")

    def test_add(
        self,
        patch_tempfile: Callable[[str], None],
        add_cmd: commands.Add,
        funk_dict: Dict[str, str],
    ) -> None:
        """Tests add command."""
        assert add_cmd.funk is not None
        funk_cmd_string = funk_dict[add_cmd.funk]
        patch_tempfile(funk_cmd_string)
        add_cmd()

        loaded_funks = load_funks()
        assert loaded_funks == {add_cmd.funk: funk_cmd_string}
        assert len(loaded_funks) == 1

    def test_add_empty(self, patch_tempfile: Callable[[str], None]) -> None:
        """Tests that add command does NOT accept empty funk definitions."""
        funk_cmd_string = ""
        patch_tempfile(funk_cmd_string)

        with pytest.raises(errors.FunkyError):
            cmd = commands.Add(["new_funk"])
            cmd()

    @pytest.mark.usefixtures("cleandir", "fake_db")
    def test_edit(
        self, patch_tempfile: Callable[[str], None], edit_cmd: commands.Edit
    ) -> None:
        """Tests edit command."""
        edited_cmd_string = "TEST COMMAND STRING"
        patch_tempfile(edited_cmd_string)

        edit_cmd()

        loaded_funks = load_funks()
        assert edit_cmd.funk is not None
        assert loaded_funks[edit_cmd.funk] == '{} "$@"'.format(
            edited_cmd_string
        )

    @pytest.mark.usefixtures("cleandir", "fake_db")
    def test_edit_empty(
        self, patch_tempfile: Callable[[str], None], funk_dict: Dict[str, str]
    ) -> None:
        """
        Tests that a funk definition left empty results in the funk being
        removed.

        This function also tests that the funky database is deleted after all
        local funks have been removed.
        """
        edited_cmd_string = ""

        assert os.path.isfile(commands.Command.FUNKY_DB_FILENAME)

        for i, funk in enumerate(funk_dict):
            patch_tempfile(edited_cmd_string)
            cmd = commands.Edit([funk])
            assert len(cmd.funk_dict) == (len(funk_dict) - i)
            cmd()

        assert not os.path.isfile(commands.Command.FUNKY_DB_FILENAME)

    @pytest.mark.usefixtures("cleandir", "fake_db")
    def test_edit_format(
        self, patch_tempfile: Callable[[str], None], funk_dict: Dict[str, str]
    ) -> None:
        """Tests that the edit command reformats command strings when needed."""
        edited_cmd_string = "EDITED CMD STRING"

        patch_tempfile(edited_cmd_string)

        some_funk = list(funk_dict.keys())[0]
        cmd = commands.Edit([some_funk])
        cmd()

        loaded_funks = load_funks()
        assert loaded_funks[some_funk] == '{} "$@"'.format(edited_cmd_string)

    @pytest.mark.usefixtures("cleandir", "fake_db")
    def test_edit_funk_not_defined(self) -> None:
        """Tests that the edit command fails when the funk is not defined."""
        with pytest.raises(errors.FunkNotDefinedError):
            edit_cmd = commands.Edit(["bad_funk"])
            edit_cmd()

    @pytest.fixture
    def add_cmd(self, args: Args) -> commands.Add:
        """Builds and returns 'add' command."""
        cmd = commands.Add(args.args, color=args.color)
        return cmd

    @pytest.fixture
    def edit_cmd(self, args: Args) -> commands.Edit:
        """Builds and returns 'edit' command."""
        cmd = commands.Edit(args.args, color=args.color)
        return cmd

    @pytest.fixture
    def patch_tempfile(self, mocker: MockerFixture) -> Callable[[str], None]:
        """Setup sp and tempfile patches for testing edit and add commands."""
        tempfile = mocker.patch("funky.commands.tempfile")

        def _patch_tempfile(cmd_string: str) -> None:
            tmpfilename = "/tmp/test_edit.txt"
            with open(tmpfilename, "w") as f:
                f.write(cmd_string)

            fileMock = mock.Mock(name="fileMock")
            fileMock.name = tmpfilename
            tempfile.NamedTemporaryFile = mock.Mock()
            tempfile.NamedTemporaryFile.return_value = fileMock

        return _patch_tempfile


@pytest.mark.usefixtures("cleandir", "fake_db")
class TestRename:
    def test_rename(
        self, rename_cmd: commands.Rename, funk_dict: Dict[str, str]
    ) -> None:
        """Test rename command."""
        assert rename_cmd.funk is not None
        old_cmd_string = funk_dict[rename_cmd.funk]
        rename_cmd()
        loaded_funks = load_funks()
        assert loaded_funks[rename_cmd.args[0]] == old_cmd_string

    def test_rename_fail(self) -> None:
        """Test that rename command fails when OLD funk does not exist."""
        cmd = commands.Rename(["bad_funk", "NEW"])
        with pytest.raises(errors.FunkNotDefinedError):
            cmd()

    @pytest.mark.parametrize("y_or_n", ["y", "n"])
    @mock.patch("funky.utils.getch")
    def test_rename_overwrite(
        self,
        getch: mock.MagicMock,
        y_or_n: str,
        funk_dict: Dict[str, str],
    ) -> None:
        """Test that rename overwrites existing function names properly."""
        getch.side_effect = lambda x: y_or_n
        fnames = list(funk_dict)
        OLD, NEW = fnames[0], fnames[1]
        cmd = commands.Rename([OLD, NEW])
        cmd()

        loaded_funks = load_funks()
        if y_or_n == "y":
            cmd_string = funk_dict[OLD]
        else:
            cmd_string = funk_dict[NEW]

        assert loaded_funks[NEW] == cmd_string

    @pytest.fixture
    def rename_cmd(self, args: Args) -> commands.Rename:
        """Builds and returns 'rename' command"""
        cmd = commands.Rename([args.args[0], "NEW"])
        return cmd


@pytest.mark.usefixtures("cleandir", "fake_db")
class TestShow:
    def test_show(
        self, capsys: CaptureFixture, show_cmd: commands.Show
    ) -> None:
        """Tests show command."""
        show_cmd()
        captured = capsys.readouterr()
        assert captured.out == getattr(show_cmd, "expected")

    def test_show_prefix(
        self, capsys: CaptureFixture, show_expected: Dict[str, str]
    ) -> None:
        """Tests show command when funk prefix is used."""
        cmd = commands.Show("T..")
        cmd()
        captured = capsys.readouterr()
        assert captured.out == "{}{}".format(
            show_expected["T"], show_expected["TT"]
        )

    def test_show_verbose(
        self, capsys: CaptureFixture, funk_dict: Dict[str, str]
    ) -> None:
        """Tests show command with verbose output."""
        cmd = commands.Show(None, verbose=True)
        cmd()
        captured = capsys.readouterr()

        count_no_newlines = 0
        for cmd_string in funk_dict.values():
            if "\n" not in cmd_string:
                count_no_newlines += 1

        assert captured.out.count("unalias") == len(funk_dict)

    def test_show_all(
        self, capsys: CaptureFixture, show_expected: Dict[str, str]
    ) -> None:
        """Tests show command when no specific funk is provided."""
        show_cmd = commands.Show(None, color=False)
        show_cmd()
        expected = "{0}{1}{2}".format(
            show_expected["multiline"], show_expected["T"], show_expected["TT"]
        )
        captured = capsys.readouterr()
        assert captured.out == expected

    def test_show_failure__NOT_DEFINED(self) -> None:
        """Tests show command fails when the requested funk is not defined."""
        with pytest.raises(errors.FunkNotDefinedError):
            show_cmd = commands.Show("bad_funk", False)
            show_cmd()

    def test_show_failure__NONE_ARE_DEFINED(self) -> None:
        """
        Tests show command fails when the given funk pattern matches no funks.

        A funk pattern is (at the time of this writing) any string ending in
        '..'.
        """
        with pytest.raises(errors.FunkNotDefinedError):
            show_cmd = commands.Show("bad_funk_pattern..", False)
            show_cmd()

    # Disables the 'fake_db' fixture for this test.
    @pytest.mark.parametrize("fake_db", [None])
    def test_show_failure__NO_DB(self, show_cmd: commands.Show) -> None:
        """
        Tests show command fails properly when no local funk database exists.
        """
        with pytest.raises(errors.FunkNotDefinedError):
            show_cmd()

    @pytest.fixture
    def show_cmd(
        self, args: Args, show_expected: Dict[str, str]
    ) -> commands.Show:
        """Builds and returns show command."""
        cmd = commands.Show(args.args, color=args.color)
        setattr(cmd, "expected", show_expected[args.args[0]])
        return cmd

    @pytest.fixture
    def show_expected(self, funk_dict: Dict[str, str]) -> Dict[str, str]:
        """
        Expected results for show command tests BEFORE prefix matching feature
        was added.
        """
        result = {
            "T": "T() {{ {0}; }}\n".format(funk_dict["T"]),
            "TT": "TT() {{ {0}; }}\n".format(funk_dict["TT"]),
            "multiline": "multiline() {{\n\t{0}\n}}\n".format(
                funk_dict["multiline"].replace("\n", "\n\t")
            ),
        }

        return result


@pytest.mark.usefixtures("cleandir", "fake_db")
class TestRemove:
    def test_remove(self, remove_cmd: commands.Remove) -> None:
        """Tests remove command."""
        remove_cmd()
        loaded_funks = load_funks()
        assert remove_cmd.funk not in loaded_funks

    def test_remove_last(self, funk_dict: Dict[str, str]) -> None:
        """
        Tests that local funk database is removed when last funk is removed.
        """
        assert os.path.isfile(commands.Command.FUNKY_DB_FILENAME)

        for funk in funk_dict:
            remove_cmd = commands.Remove(funk)
            remove_cmd()

        assert not os.path.isfile(commands.Command.FUNKY_DB_FILENAME)

    @pytest.mark.parametrize("y_or_n", ["y", "n"])
    @mock.patch("funky.utils.getch")
    def test_remove_all(self, getch: mock.MagicMock, y_or_n: str) -> None:
        """
        Tests that the local funk database is removed when no funk is provided
        and the user confirms.
        """
        getch.side_effect = lambda x: y_or_n

        assert os.path.isfile(commands.Command.FUNKY_DB_FILENAME)

        remove_cmd = commands.Remove(None)
        remove_cmd()

        isfile = os.path.isfile(commands.Command.FUNKY_DB_FILENAME)
        if y_or_n == "y":
            expected = not isfile
        else:
            expected = isfile

        assert expected

    def test_remove_funk_not_exist(self) -> None:
        """Tests remove command fails when funk doesn't exist."""
        with pytest.raises(errors.FunkNotDefinedError):
            remove_cmd = commands.Remove(["bad_funk"])
            remove_cmd()

    @pytest.fixture
    def remove_cmd(self, args: Args) -> commands.Remove:
        """Builds and returns 'remove' command."""
        cmd = commands.Remove(args.args, color=args.color)
        return cmd


###############################################################################
#  Pytest Fixtures                                                            #
###############################################################################
@pytest.fixture
def fake_db(funk_dict: Dict[str, str]) -> Iterator[Dict[str, str]]:
    """Setup/teardown a local funk database"""
    _fake_db = _fake_db_factory(commands.Command.FUNKY_DB_FILENAME, funk_dict)
    for item in _fake_db():
        yield item


def _fake_db_factory(
    DB_FILENAME: str, funk_dict_builder: Dict[str, str]
) -> Callable[[], Iterator[Dict[str, str]]]:
    """Builds a generator fixture for creating a fake database."""

    def _fake_db() -> Iterator[Dict[str, str]]:
        my_funk_dict = funk_dict_builder
        with open(DB_FILENAME, "w") as f:
            json.dump(my_funk_dict, f)
        yield my_funk_dict
        try:
            os.remove(DB_FILENAME)
        except OSError:
            pass

    return _fake_db


@pytest.fixture
def funk_dict() -> Dict[str, str]:
    funk_dict_ = {
        "multiline": "echo Hello\necho world!",
        "T": "echo RUN $1",
        "TT": "echo CHICKEN $@",
    }
    return funk_dict_


@pytest.fixture(
    params=[
        (["T", "PROGRAM"], False),
        (["TT", "WING"], False),
        (["multiline"], False),
    ],
    ids=["T", "TT", "multiline"],
)
def args(request: SubRequest) -> Args:
    """Returns a named tuple of command arguments and expected results."""
    return Args(request.param[0], request.param[1])


###############################################################################
#  Utility Functions                                                          #
###############################################################################
def load_funks() -> Dict[str, str]:
    """Loads funks from database file"""
    with open(commands.Command.FUNKY_DB_FILENAME, "r") as f:
        loaded_funks: Dict[str, str] = json.load(f)
    return loaded_funks
