from .db.postgre_prompt_dao import PromptDao


class CommandHandler():
    DEFAULT_MESSAGE = '''
    Available commands:
        !show
            show Q&A
        !add q/a
            add Q&A
        !delete q/a
            delete Q&A
    '''

    def __init__(self):
        self.dao = PromptDao()

    def parse_msg(self, msg):
        space = msg.find(" ")
        cmd = msg[:space] if space != -1 else msg
        args = msg[space+1:] if space != -1 else ""
        return (cmd, args)

    def handle(self, user_id, msg):
        resp = CommandHandler.DEFAULT_MESSAGE
        cmd, args = self.parse_command(msg)
        if cmd == "!show":
            resp = "Your questions and answers:\n"
            prompt = self.dao.getPromptByUser(user_id)
            for hint in prompt.get("hints", []):
                resp = resp + "question: " + \
                    hint["question"] + "\n" + \
                    "answer: " + hint["answer"] + "\n"
        elif cmd == "!add":  # ADD
            qalist = cmd.split("/")
            if len(qalist) == 2:
                prompt = self.dao.getPromptByUser(user_id)
                for hint in prompt["hints"]:
                    if hint["question"] == qalist[0]:
                        hint["answer"] = qalist[1]
                        break
                else:
                    new_hint = {"question": qalist[0], "answer": qalist[1]}
                    prompt["hints"].append(new_hint)
                self.dao.savePrompt(prompt)
                resp = "q/a added"
        elif cmd == "!delete":
            qalist = cmd.split("/")
            if len(qalist) == 2:
                prompt = self.dao.getPromptByUser(user_id)
                filtered_hints = filter(lambda hint: not (hint["question"] == qalist[0]
                                                          and hint["answer"] == qalist[1]), prompt["hints"])
                prompt["hints"] = list(filtered_hints)
                self.dao.savePrompt(prompt)
                resp = "q/a deleted"

        return resp
