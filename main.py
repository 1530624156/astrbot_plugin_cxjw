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
        # {'commandText': '小星小星', 'sub_config': {'apiUrl': 'http://localhost:8080/api/qqMsg', 'enc': 'mavis'}}
        api_url:str = self.config.sub_config["apiUrl"]
        api_enc:str = self.config.sub_config["enc"]
        message_str = event.message_str
        group_id = event.get_session_id()
        user_id = event.get_sender_id()
        #  判断消息是否以指定命令开头并且是群聊消息
        if message_str.startswith(command_text):
            response = httpx.post(api_url,json={"message":message_str,"group_id":group_id,"user_id":user_id})
            yield event.plain_result(f"Hello, {user_name}:{user_id}in Group{group_id}, 你发了 {message_str}{api_url}{api_enc}!") 
        
       
    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
