#import os
#import ast
#from llm_client import HelloAgentsLLM
from dotenv import load_dotenv
#from typing import List, Dict


import re
from llm_client import HelloAgentsLLM
from tools import ToolExecutor, search

try:
    load_dotenv()
except FileNotFoundError:
    print("警告：未找到 .env 文件，将使用系统环境变量。")
except Exception as e:
    print(f"警告：加载 .env 文件时出错: {e}")
# 这一步是一个保底处理 目的是为了检查 是否能找到我的api文件，load_dotenv()：就是去翻找 .env 文件，把里面的密码装进系统环境变量里。



REACT_PROMPT_TEMPLATE = """
请注意，你是一个有能力调用外部工具的智能助手。

可用工具如下：
{tools}

请严格按照以下格式进行回应：

Thought: 你的思考过程，用于分析问题、拆解任务和规划下一步行动。
Action: 你决定采取的行动，必须是以下格式之一：
- `{{tool_name}}[{{tool_input}}]`：调用一个可用工具。
- `Finish[最终答案]`：当你认为已经获得最终答案时。
- 当你收集到足够的信息，能够回答用户的 最终问题时，你必须在`Action:`字段后使用 `Finish[最终答案]` 来输出最终答案。


现在，请开始解决以下问题：
Question: {question}
History: {history}
"""





class ReActAgent:





    def __init__(self, llm_client: HelloAgentsLLM, tool_executor: ToolExecutor, max_steps: int = 5):
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.max_steps = max_steps
        self.history = []
        #和大模型连接上
        #连接一个自己的搜索工具
        #固定最大搜索次数
        #历史思考记录表








    def run(self, question: str):
        self.history = []
        current_step = 0
    #def 主入口方法。就像你按下了汽车的“启动”按钮，把问题丢进去，整个循环就开始转动了
        #清空记事本
        #运行次数一开始是0
        while current_step < self.max_steps:
            current_step += 1
            print(f"\n--- 第 {current_step} 步 ---")
        #while 次数小于定义的最大次数就一直跑
            #次数加1
            #打印次数让用户看到
            tools_desc = self.tool_executor.getAvailableTools()
            history_str = "\n".join(self.history)
            prompt = REACT_PROMPT_TEMPLATE.format(tools=tools_desc, question=question, history=history_str)
            #获取工具
            #用换行符（\n）把历史拼成一根长长的字符串
            #组装 铁律 工具 问题 历史思考纪录
            messages = [{"role": "user", "content": prompt}]
            response_text = self.llm_client.think(messages=messages)
            if not response_text:
                print("错误：LLM未能返回有效响应。");
                break
            #打包信息
            #打包信息送给大模型
            #if not 没有回应
                #打印无回应
                #结束
            thought, action = self._parse_output(response_text)
            if thought: print(f"🤔 思考: {thought}")
            if not action: print("警告：未能解析出有效的Action，流程终止。"); break
            #回应中提取思考和行动
            #if 思考 打印思考
            #if not 行动 警告 结束
            if action.startswith("Finish"):
                # 如果是Finish指令，提取最终答案并结束
                final_answer = self._parse_action_input(action)
                print(f"🎉 最终答案: {final_answer}")
                return final_answer
            #if 有行动 看看是不是以finish开头的
                #最终答案为 action
                #打印 最终答案
                #return
            tool_name, tool_input = self._parse_action(action)
            if not tool_name or not tool_input:
                self.history.append("Observation: 无效的Action格式，请检查。");
                continue
            #提取 工具名字 和工具参数 从大模型中的行动文本
            #if not 工具
                #思考历史记录加上记录 continue继续循环
                #continue
            print(f"🎬 行动: {tool_name}[{tool_input}]")
            tool_function = self.tool_executor.getTool(tool_name)
            observation = tool_function(tool_input) if tool_function else f"错误：未找到名为 '{tool_name}' 的工具。"
            #打印一句：“行动：用 工具名 去查 参数”（让用户看到）
            #去百宝箱（tool_executor）里，把那个叫 工具名 的工具（函数）掏出来
            #把那个叫 工具名 的工具（函数）用工具参数 来执行
            print(f"👀 观察: {observation}")
            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {observation}")
            #把刚才的行动和结果，写进记事本：
            #记事本加上 "Action: 行动"
            #记事本加上 "Observation: 观察结果"
        print("已达到最大步数，流程终止。")
        return None
        #如果 while 循环一直跑，跑够了 max_steps 次数还没交卷：打印 “已达到最大步数，流程终止”
        #返回 None （告诉老板，任务失败了）








    def _parse_output(self, text: str):
        # Thought: 匹配到 Action: 或文本末尾
        thought_match = re.search(r"Thought:\s*(.*?)(?=\nAction:|$)", text, re.DOTALL)
        # Action: 匹配到文本末尾
        action_match = re.search(r"Action:\s*(.*?)$", text, re.DOTALL)
        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        return thought, action
    #def 文字提取函数
        #从大模型返回的语言中找到思考的部分 （这一部分是'回应中提取思考和行动'68行 这一步来的 我们在运行到96行的时候 代码转到提取思考和行动这一步）【执行来源】：由 run 方法里的 “thought, action = self._parse_ou
        #从大模型返回的语言中找到行动的部分
        #提取出思考 如果无思考返回none
        #提取出行动 如果无行动返回none
        #返回思考和行动


    def _parse_action(self, action_text: str):
        match = re.match(r"(\w+)\[(.*)\]", action_text, re.DOTALL)
        return (match.group(1), match.group(2)) if match else (None, None)
    #def 工具提取函数（这一步是由工具提取函数 tool_name, tool_input = self._parse_action(action) 111 行 发生的跳转
        #用字符串模板筛选出 要处理的字符串 拿模具去套这段文本
        #return 字符串里面的工具 if 匹配就ok else就none


    def _parse_action_input(self, action_text: str):
        match = re.match(r"\w+\[(.*)\]", action_text, re.DOTALL)
        return match.group(1) if match else ""
    #def 这一步是由finish提取函数- (最终答案为 action) final_answer = self._parse_action_input(action)104行 发生的跳转
        #用字符串模板筛选出 要处理的字符串 拿模具去套这段文本
        #return 结果 if 匹配就ok else就none





if __name__ == '__main__':
    llm = HelloAgentsLLM()
    tool_executor = ToolExecutor()
    search_desc = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    tool_executor.registerTool("Search", search_desc, search)
    agent = ReActAgent(llm_client=llm, tool_executor=tool_executor)
    question = "我明天要去苏州出差，请帮我查一下苏州明天的天气，并顺便推荐两个苏州必吃的老字号面馆."
    agent.run(question)
#if 入场保护 只有我直接被点开运行时，下面的代码才会生效。
    #连接到大模型
    #拿出工具箱
    #搜索函数和说明书放在工具箱子里面
    #执行 代码 用（连接到大模型）和（搜索函数和说明书放在工具箱子里面）__init__(self, llm_client: HelloAgentsLLM, tool_executor: ToolExecutor, max_steps: int = 5):
    #执行 代码 写一份问题：run(self, question: str):