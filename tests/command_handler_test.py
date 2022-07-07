from src.command_handler import CommandHandler


def test_handle_success(mocker):
    mock_dao = mocker.MagicMock()
    mock_dao.savePrompt.return_value = None
    handler = CommandHandler(mock_dao)

    msg = "!show"
    # assign new response every time, since list is mutable, might have side effect if reuse the same object
    mock_dao.getPromptByUser.return_value = {
        "hints": [{"question": "q1", "answer": "a1"}]}
    actual = handler.handle("user_123", msg)
    assert actual.startswith("Your questions and answers:")

    msg = "!add q2/a2"
    mock_dao.getPromptByUser.return_value = {
        "hints": [{"question": "q1", "answer": "a1"}]}
    actual = handler.handle("user_123", msg)
    assert actual == "question: q2, answer: a2\nadded"
    mock_dao.savePrompt.assert_called_with(
        {"hints": [{"question": "q1", "answer": "a1"}, {"question": "q2", "answer": "a2"}]})

    # add command should overwrite answer if question exists
    msg = "!add q1/a123"
    mock_dao.getPromptByUser.return_value = {
        "hints": [{"question": "q1", "answer": "a1"}]}
    actual = handler.handle("user_123", msg)
    assert actual == "question: q1, answer: a123\nadded"
    mock_dao.savePrompt.assert_called_with(
        {"hints": [{"question": "q1", "answer": "a123"}]})

    msg = "!add"
    actual = handler.handle("user_123", msg)
    assert actual == "invalid q/a format, please input again"

    msg = "!delete q1/a1"
    mock_dao.getPromptByUser.return_value = {
        "hints": [{"question": "q1", "answer": "a1"}]}
    actual = handler.handle("user_123", msg)
    assert actual == "question: q1, answer: a1\ndeleted"
    mock_dao.savePrompt.assert_called_with({"hints": []})

    msg = "!delete"
    actual = handler.handle("user_123", msg)
    assert actual == "all q/a deleted"

    msg = "!delete abcd"
    actual = handler.handle("user_123", msg)
    assert actual == "invalid q/a format, please input again"
