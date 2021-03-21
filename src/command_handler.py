from .db.postgre_prompt_dao import PromptDao


class CommandHandler():
    # user_states
    #   INIT(1): show cmd list => 1 show q/a, 2 goto ADD, 3 goto DELETE
    #   ADD(2): add q/a => enter q/a or press 9 goto state INIT
    #   DELETE(3): delete q/a => enter a question to delete or press 9 goto state INIT
    user_states = {}

    def __init__(self):
        self.dao = PromptDao()

    def handle(self, user_id, cmd):
        if CommandHandler.user_states.get(user_id) is None:
            CommandHandler.user_states[user_id] = 1
        current_state = CommandHandler.user_states[user_id]

        print("state:", current_state, "cmd:", cmd)
        resp = ""
        if current_state == 1:  # INIT
            if cmd == "1":  # show q/a
                resp = "q/a list:\n"
                prompt = self.dao.getPromptByUser(user_id)
                for hint in prompt.get("hints", []):
                    resp = resp + "question: " + \
                        hint["question"] + "\n" + \
                        "answer: " + hint["answer"] + "\n"
            elif cmd == "2":  # add q/a
                resp = "please type question and answer in q/a format to add or 9 to cancel"
                current_state = 2  # goto ADD
            elif cmd == "3":  # delete q/a
                resp = "please type question and answer in q/a format to delete or 9 to cancel"
                current_state = 3  # goto DELETE
            else:  # unknown cmd
                resp = "available cmds:\n" \
                    + "1: show q/a\n" \
                    + "2: add q/a\n" \
                    + "3: delete q/a\n"
        elif current_state == 2:  # ADD
            qalist = cmd.split("/")
            if cmd == "9":
                resp = "available cmds:\n" \
                    + "1: show q/a\n" \
                    + "2: add q/a\n" \
                    + "3: delete q/a\n"
                current_state = 1
            elif len(qalist) == 2:
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
                current_state = 1
            else:
                resp = "please type question and answer in q/a format to add or 9 to cancel"
        elif current_state == 3:  # DELETE
            qalist = cmd.split("/")
            if cmd == "9":
                resp = "available cmds:\n" \
                    + "1: show q/a\n" \
                    + "2: add q/a\n" \
                    + "3: delete q/a\n"
                current_state = 1
            elif len(qalist) == 2:
                prompt = self.dao.getPromptByUser(user_id)
                filtered_hints = filter(lambda hint: not (hint["question"] == qalist[0]
                       and hint["answer"] == qalist[1]), prompt["hints"])
                prompt["hints"] = list(filtered_hints)
                self.dao.savePrompt(prompt)
                resp = "q/a deleted"
                current_state = 1
            else:
                resp = "please type question and answer in q/a format to delete or 9 to cancel"
        else:  # UNKNOWN
            current_state = 1  # reset
            resp = "wrong state"

        CommandHandler.user_states[user_id] = current_state
        return resp
