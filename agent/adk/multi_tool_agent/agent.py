import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


# NOTE:

# ref:
# - https://google.github.io/adk-docs/get-started/quickstart/
# - https://docs.litellm.ai/docs/providers/deepseek

# requirements:
# - pip install google-adk
# - pip install litellm

# run agent:
# adk web
# adk run multi_tool_agent


def get_weather(city: str) -> dict:
    """获取指定城市的当前天气报告

    Args:
        city (str): 需要查询天气的城市名称

    Returns:
        dict: 包含状态和结果/错误消息的字典
    """
    if city == "杭州":
        return {
            "status": "success",
            "report": "杭州天气晴朗，气温 25 摄氏度（77 华氏度）"
        }
    else:
        return {
            "status": "error",
            "error_message": f"未找到'{city}'的天气信息"
        }


def get_current_time(city: str) -> dict:
    """获取指定城市的当前时间

    Args:
        city (str): 需要查询时间的城市名称

    Returns:
        dict: 包含状态和结果/错误消息的字典
    """
    if city == "杭州":
        tz_identifier = "Asia/Shanghai"
    else:
        return {
            "status": "error",
            "error_message": f"未找到{city}的时区信息"
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'{city}当前时间: {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


root_agent = Agent(
    name="weather_time_agent",
    model=LiteLlm(  # 适配 DeepSeek LLM
        model="deepseek/deepseek-chat",  # 注意：模型名称应该是：provider + / + model_name
        # base_url="...",
        api_key="替换成你的 API Key",
    ),
    description="用于回答城市时间和天气问题的助手代理",
    instruction="你是一个能帮助用户查询城市时间和天气的智能助手",
    tools=[get_weather, get_current_time],
)
