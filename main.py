from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger,AstrBotConfig
import httpx

@register("cxjw", "Mavis", "超星集团教务部门自用插件", "0.0.1")
class MyPlugin(Star):
    def __init__(self, context: Context,config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        print(self.config)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
    
    # 消息处理入口
    @filter.event_message_type(filter.EventMessageType.ALL)
    async def execMsg(self, event: AstrMessageEvent):
        # handler描述
        """统一入口插件""" 
        user_name = event.get_sender_name()
        # 获取配置
        command_text:str = self.config.commandText
        api_url:str = self.config.sub_config["apiUrl"]
        api_enc:str = self.config.sub_config["enc"]
        message_str = event.message_str
        group_id = event.get_session_id()
        user_id = event.get_sender_id()
        #  判断消息是否以指定命令开头并且是群聊消息
        if message_str.startswith(command_text):
            # 设置超时时间
            timeout = httpx.Timeout(timeout=30.0, connect=10.0)
            response = httpx.post(api_url,json={"context":message_str,"groupId":group_id,"userId":user_id,"enc":api_enc},timeout=timeout)
            result:str = response.text
            # 发送消息
            yield event.plain_result(f"{result}") 
        
       
    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
