class NFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        """
        初始化 NFA
        :param states: 状态集合
        :param alphabet: 字母表（输入集合）
        :param transitions: 转换函数，格式为 {状态: {事件: [目标状态列表]}}
        :param start_state: 初始状态
        :param accept_states: 接受状态集合
        """
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = set(accept_states)
        self.dominance_relations = {}  # 用于存储状态间的支配关系

    def transition(self, current_state, event):
        """
        根据输入事件执行状态转换
        imput:
            :param current_state: 当前状态
            :param event: 输入事件
        output:
            :return: 转换后的状态列表，如果没有定义转换则返回空列表
        """
        if current_state in self.transitions and event in self.transitions[current_state]:
            return self.transitions[current_state][event]
        return []  # 无转换时返回空列表

    def dominates(self, state1, state2):
        """
        判断 state1 是否支配 state2
        :param state1: 状态1
        :param state2: 状态2
        :return: True 如果 state1 ⪯ state2，否则 False
        """
        for event in self.alphabet:  # 遍历字母表
            delta1 = self.transition(state1, event)  # 从 state1 的转移
            delta2 = self.transition(state2, event)  # 从 state2 的转移
            
            # 检查支配条件
            if delta2 == []:  # 条件1: delta(state2, event) = 空集
                continue
            elif delta1 == delta2:  # 条件2: 转移结果相同
                continue
            elif state1 in delta1 and state2 in delta2:  # 条件3: 自环
                continue
            else:
                return False  # 如果任何一个事件不满足支配条件，返回 False
        return True  # 所有事件都满足支配条件，返回 True

    def compute_dominance_relations(self):
        """
        计算并存储状态间的支配关系
        """
        self.dominance_relations = {}  # 清空之前的记录
        for s1 in self.states:
            for s2 in self.states:
                self.dominance_relations[(s1, s2)] = self.dominates(s1, s2)

    def get_dominance_matrix(self):
        """
        获取支配关系矩阵
        :return: 支配关系的二维矩阵（列表格式）
        """
        matrix = []
        for s1 in self.states:
            row = []
            for s2 in self.states:
                row.append(self.dominance_relations.get((s1, s2), False))
            matrix.append(row)
        
        self.dominance_matrix = matrix

        print("支配关系矩阵:")
        print("    ", "     ".join(self.states))
        for state, row in zip(self.states, self.dominance_matrix):
            print(state, row)
        
        pass

    def domineState(self, s):
        """
        返回状态s支配的状态
        """
        ans = []
        for index, item in enumerate(self.dominance_matrix[int(s[-1])]):
            if item and index != int(s[-1]):
                ans.append(self.states[index])
        return ans
    
    def beDominedState(self, s):
        """
        返回状态s被哪些状态支配
        """
        ans = []
        for index, item in enumerate(self.dominance_matrix):
            if item[int(s[-1])] and index != int(s[-1]): # int(s[-1]): 状态s所对应的序号
                ans.append(self.states[index])
        return ans

if __name__ == "__main__":
    # 定义 NFA 元素
    states = ["s0", "s1", "s2", "s3", "s4", "s5"]
    alphabet = {"c", "w", "b", "s"}
    transitions = {
        "s0": {"c": ["s2"], "w": ["s1"], "b": ["s1"]},
        "s1": {"w": ["s1"], "b": ["s1"], "s": ["s4"]},
        "s2": {"c": ["s2"], "w": ["s3"]},
        "s3": {"w": ["s3"], "b": ["s3"], "s": ["s4"]},
        "s4": {"s": ["s4"], "w": ["s5"]},
        "s5": {"w": ["s5"], "b": ["s5"]},
    }
    start_state = "s0"
    accept_states = {"s1", "s3", "s5"}

    # 创建 NFA
    nfa = NFA(states, alphabet, transitions, start_state, accept_states)

    # 计算并记录支配关系
    nfa.compute_dominance_relations()

    # 打印支配关系矩阵
    nfa.get_dominance_matrix()


    print("s1所支配的状态集合：{}".format(nfa.domineState('s1')))
    print("支配s1的状态集合：{}".format(nfa.beDominedState('s1')))
    print("支配s5的状态集合：{}".format(nfa.beDominedState('s5')))


    # # 打印支配关系字典
    # print("\n支配关系字典:")
    # for key, value in nfa.dominance_relations.items():
    #     print(f"{key[0]} ⪯ {key[1]}: {value}")

