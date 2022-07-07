from .db.postgre_prompt_dao import PromptDao


class CommandHandler():
    DEFAULT_MESSAGE = '''Available commands:
!show !S
    show all Q&As

!add !A q/a
    overwrite answer if question already exists else add a new Q&A

!delete !D [q/a]
    delete specific Q&A or delete all Q&As if not specified
'''

    def __init__(self, dao=None):
        self.dao = dao if dao else PromptDao()

    def parse_command(self, msg):
        space = msg.find(" ")
        cmd = msg[:space] if space != -1 else msg
        args = msg[space+1:] if space != -1 else ""
        return (cmd, args)

    def handle(self, user_id, msg):
        resp = CommandHandler.DEFAULT_MESSAGE
        cmd, args = self.parse_command(msg)
        if cmd == "!show" or cmd == "!S":
            resp = "Your questions and answers:\n"
            prompt = self.dao.getPromptByUser(user_id)
            for hint in prompt.get("hints", []):
                resp = resp + "question: " + \
                    hint["question"] + "\n" + \
                    "answer: " + hint["answer"] + "\n"
        elif cmd == "!add" or cmd == "!A":
            qalist = args.split("/")
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
                resp = f"question: {qalist[0]}, answer: {qalist[1]}\nadded"
            else:
                resp = "invalid q/a format, please input again"
        elif cmd == "!delete" or cmd == "!D":
            qalist = args.split("/")
            if not args:
                self.dao.deletePromptByUser(user_id)
                resp = "all q/a deleted"
            elif len(qalist) == 2:
                prompt = self.dao.getPromptByUser(user_id)
                filtered_hints = filter(lambda hint: not (hint["question"] == qalist[0]
                                                          and hint["answer"] == qalist[1]), prompt["hints"])
                prompt["hints"] = list(filtered_hints)
                self.dao.savePrompt(prompt)
                resp = f"question: {qalist[0]}, answer: {qalist[1]}\ndeleted"
            else:
                resp = "invalid q/a format, please input again"
        return resp
