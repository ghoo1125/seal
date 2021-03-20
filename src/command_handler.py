from .db.prompt_dao import PromptDao


class CommandHandler():
    def __init__(self):
        self.dao = PromptDao()

    def handle(self, user_id, cmd):
        print("user_id: ", user_id)
        print("cmd: ", cmd)

        if cmd == "1":
            mock_prompt = {"user_id": user_id, "hints": [
                {"question": "abc", "answer": cmd}]}
            self.dao.savePrompt(mock_prompt)
            return "ok"
        elif cmd == "2":
            prompt = self.dao.getPromptByUser(user_id)
            resp = "resp data:\n"
            for hint in prompt["hints"]:
                resp = resp + "question: " + \
                    hint["question"] + "\n" + \
                    "answer: " + hint["answer"] + "\n"
            return resp
        else:
            return "cmd not found"
