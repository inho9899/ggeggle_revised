from src.vars import *

class UserCustom :
    def __init__(self, A_exist, A_None, B_start, B_end, C_option) :
        self.A_exist = A_exist
        self.A_None = A_None
        self.B_start = B_start
        self.B_end = B_end
        self.C_option = C_option
    

class UserCustomManager:
    def __init__(self):
        self.entries = []  # 누적된 입력 데이터를 저장할 리스트

    def add_entry(self, A_exist, A_None, B_start, B_end, C_option):
        res = ""
        if A_exist:
            res += f"**{A_exist}** 이(가) 있고 "
        if A_None:
            res += f"**{A_None}** 이(가) 제외된 경우\n\n"
        if B_start:
            res += f"**{B_start}** 로 시작하고 "
        if B_end:
            res += f"**{B_end}** 로 끝나는 모든 단어는\n\n"
        if C_option.isdigit():
            res += f"글자 계산 우선순위에서 숫자 **{C_option}** 으로 계산\n\n"
        else:
            res += f"**{C_option}**\n\n"

        user_custom_map.append(UserCustom(A_exist, A_None, B_start, B_end, C_option))

        entry = res.strip()

        self.entries.append(entry)
        # print("추가된 커스텀 항목:\n", entry)
        # 누적된 항목들을 개행으로 구분하여 하나의 문자열로 반환
        return "\n\n---\n\n".join(self.entries)
