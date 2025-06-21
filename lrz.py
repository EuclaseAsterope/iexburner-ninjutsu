from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Star, register
from astrbot.api import logger
import os


@register(
    "astrbot_plugin_ninjutsu",
    "忍术语音插件",
    "通过指令释放忍术语音，包含藏经阁功能",
    "1.2.0",
    "https://github.com/yourname/astrbot_plugin_ninjutsu"
)
class NinjutsuPlugin(Star):
    def __init__(self, context):
        super().__init__(context)
        # 获取插件目录路径
        self.plugin_dir = os.path.dirname(os.path.abspath(__file__))
        # 设置音频文件存放目录
        self.sources_dir = os.path.join(self.plugin_dir, "sources")
        # 确保目录存在
        os.makedirs(self.sources_dir, exist_ok=True)

        # 忍术名称到音频文件的映射
        # 智能音频文件映射表（中英文混合使用全拼+英文）
        # 格式: "原文件名": "目标文件名",
        self.ninjutsu_mapping = {
            "Dragon": "dragon.wav",
            "Genshin": "genshin.wav",
            "Ultra奥特曼黑手": "aotemanheishou_ultra.wav",
            "hello我闪现切你的手": "woshanxianqienideshou_hello.wav",
            "i see you": "i_see_you.wav",
            "一刀一刀燃烧刀": "yidaoyidaoranshaodao.wav",
            "一哭二闹三上吊的": "yikuernaosanshangdiaode.wav",
            "万维手": "wanweishou.wav",
            "主播那碗是翔": "zhubonawanshixiang.wav",
            "人有互动": "renyouhudong.wav",
            "今天来给大家释放忍术": "jintianlaigeidajiashifangrenshu.wav",
            "他拿的钝单手菜刀": "tanadedundanshoucaidao.wav",
            "令神龙造成烟雾": "lingshenlongzaochengyanwu.wav",
            "你别跟我吵了": "nibiegenwochaole.wav",
            "你有完没完啊": "niyouwanmeiwana.wav",
            "你爱说什么你说什么": "niaishuoshenmenishuoshenme.wav",
            "你的手渣渣废物": "nideshouzhazhafeiwu.wav",
            "你说这些屁话": "nishuozhexiepihua.wav",
            "使用罗汉手＆河水罗汉离子手": "shiyongluohanshouheshuiluohanlizishou.wav",
            "俺会是你的罗翔啊": "anhuishinideluoxianga.wav",
            "俺要立希的专辑": "anyaolixidezhuanji.wav",
            "十万条霹雳狗": "shiwantiaopiligou.wav",
            "十亿响刀落·一万刀一百万刀": "shiyixiangdaoluoyiwandaoyibaiwandao.wav",
            "十字封印": "shizifengyin.wav",
            "南十字深深封印": "nanshizishenshenfengyin.wav",
            "原神旋风术": "yuanshenxuanfengshu.wav",
            "名刀手": "mingdaoshou.wav",
            "吓我一跳我释放忍术": "xiawoyitiaowoshifangrenshu.wav",
            "吓我一跳我释放花露水": "xiawoyitiaowoshifanghualushui.wav",
            "和我←艾": "hewoai.wav",
            "咬舌头神威": "yaoshetoushenwei.wav",
            "哈佛扪心手": "hafumenxinshou.wav",
            "哈利时光术": "halishiguangshu.wav",
            "哈利波特我想死他了": "halibotewoxiangsitale.wav",
            "哈利路大旋风": "haliludaxuanfeng.wav",
            "哈利路小旋风": "haliluxiaoxuanfeng.wav",
            "哈回米那刻斯右反手": "hahuiminakesiyoufanshou.wav",
            "哈姆你会没事的呦": "hamunihuimeishideyou.wav",
            "哈姆你赶紧走吧要不然抹杀你老姥爷": "hamuniganjinzoubayaoburanmoshanilaolaoye.wav",
            "哈姆哈姆很累": "hamuhamuhenlei.wav",
            "哈姆射手": "hamusheshou.wav",
            "哈姆杀所有": "hamushasuoyou.wav",
            "哈姆爷大无影脚": "hamuyedawuyingjiao.wav",
            "哎呀凡人哎": "aiyafanrenai.wav",
            "哎呦卧槽闪现": "aiyouwocaoshanxian.wav",
            "哪个月不闹离婚，哪个月不提离婚": "neigeyuebunaolihunneigeyuebutilihun.wav",
            "啊啦我的血雾杀杀": "alawodexuewushasha.wav",
            "啊导致我射了一手我tm": "adaozhiwosheleyishouwo_tm.wav",
            "啊彗星": "ahuixing.wav",
            "啊没手使没手使": "ameishoushimeishoushi.wav",
            "啊米娜桑": "aminasang.wav",
            "啊让我流水": "arangwoliushui.wav",
            "噢Zombie": "o_zombie.wav",
            "噩耗癌细胞": "ehaoaixibao.wav",
            "四夜雷电光": "siyeleidianguang.wav",
            "回来吧我心爱的手＆影分身环绕": "huilaibawoxinaideshouyingfenshenhuanrao.wav",
            "圣剑哈姆": "shengjianhamu.wav",
            "圣眼左手": "shengyanzuoshou.wav",
            "太痛苦了": "taitongkule.wav",
            "夯手": "hangshou.wav",
            "奥义·压路": "aoyiyalu.wav",
            "奥义升龙": "aoyishenglong.wav",
            "奥特分身": "aotefenshen.wav",
            "奶芒果 柿子 大香蕉": "naimangguoshizidaxiangjiao.wav",
            "好像有兽人来袭": "haoxiangyoushourenlaixi.wav",
            "好哥哥是你大爷": "haogegeshinidaye.wav",
            "好好睡": "haohaoshui.wav",
            "好师傅哥哥他欺负我": "haoshifugegetaqifuwo.wav",
            "好无敌的哈姆": "haowudidehamu.wav",
            "好男人也没的身手": "haonanrenyemeideshenshou.wav",
            "威化乌鸦": "weihuawuya.wav",
            "安慕希": "anmuxi.wav",
            "寒泥挪燕步": "hanninuoyanbu.wav",
            "射不尽": "shebujin.wav",
            "小男孩为难为难＆哈拉少": "xiaonanhaiweinanweinanhalashao.wav",
            "岚刀一直切": "landaoyizhiqie.wav",
            "岛漩涡鸣": "daoxuanwoming.wav",
            "干嘛干嘛我韩信，看嘛看嘛干你塔": "ganmaganmawohanxinkanmakanmagannita.wav",
            "廉颇会一夜挪山": "lianpohuiyiyenuoshan.wav",
            "影分身·十字手": "yingfenshenshizishou.wav",
            "影分身十字斩＆纳米悠悠球": "yingfenshenshizizhannamiyouyouqiu.wav",
            "影暗流·幻影诺手": "yinganliuhuanyingnuoshou.wav",
            "往事如烟手": "wangshiruyanshou.wav",
            "得到所有手": "dedaosuoyoushou.wav",
            "快给我那个手": "kuaigeiwonageshou.wav",
            "快释放离子旋风": "kuaishifanglizixuanfeng.wav",
            "恒河水是我奶妈": "hengheshuishiwonaima.wav",
            "我不是人类＆我和梅西赛跑": "wobushirenleiwohemeixisaipao.wav",
            "我们谁也别还手": "womensheiyebiehuanshou.wav",
            "我多害怕你，我多怕你": "woduohaipaniwoduopani.wav",
            "我夺取心脏": "woduoquxinzang.wav",
            "我射他身上": "woshetashenshang.wav",
            "我已经没有办法": "woyijingmeiyoubanfa.wav",
            "我心情不好": "woxinqingbuhao.wav",
            "我最后一次和你对话": "wozuihouyiciheniduihua.wav",
            "我本来心情不好，我也在直播": "wobenlaixinqingbuhaowoyezaizhibo.wav",
            "我杀死你的哈姆": "woshasinidehamu.wav",
            "我没别的意思": "womeibiedeyisi.wav",
            "我没怎么注意到": "womeizenmezhuyidao.wav",
            "我爱干嘛干嘛": "woaiganmaganma.wav",
            "我真是怕": "wozhenshipa.wav",
            "我自己大好人生不过＆我最后悔的事": "wozijidahaorenshengbuguowozuihouhuideshi.wav",
            "我装上自己的ak": "wozhuangshangzijide_ak.wav",
            "我设了一个笼": "wosheleyigelong.wav",
            "我这个事情委屈太多了": "wozhegeshiqingweiqutaiduole.wav",
            "我除了不喜欢你我什么都没做错": "wochulebuxihuanniwoshenmedoumeizuocuo.wav",
            "手握彗星": "shouwohuixing.wav",
            "打CF": "da_cf.wav",
            "把自己拿来拿盐弄模糊不清": "bazijinalainayannongmohubuqing.wav",
            "提心吊胆的": "tixindiaodande.wav",
            "握握手": "wowoshou.wav",
            "握握手握握双手": "wowoshouwowoshuangshou.wav",
            "旋反离子手": "xuanfanlizishou.wav",
            "暗威·雷龙迅": "anweileilongxun.wav",
            "暗寒死术": "anhansishu.wav",
            "暗幕·引雷电": "anmuyinleidian.wav",
            "暗影魔刀": "anyingmodao.wav",
            "暗影魔刀使": "anyingmodaoshi.wav",
            "暗流shinnobi速杀内燃手": "anliusushaneiranshou_shinnobi.wav",
            "暗神雷霆": "anshenleiting.wav",
            "暗部·煞并雷鸣": "anbushabingleiming.wav",
            "暗黑尔德machine": "anheierde_machine.wav",
            "暗黑式·黑子斩＆暗黑堕落挥刀斩": "anheishiheizizhananheiduoluohuidaozhan.wav",
            "暗黑若叶睦让我松掉乐奈的手": "anheiruoyemurangwosongdiaolenaideshou.wav",
            "暗黑蕾铭": "anheileiming.wav",
            "暗龙夺魂手": "anlongduohunshou.wav",
            "曼巴导弹": "manbadaodan.wav",
            "杀意的烟雾": "shayideyanwu.wav",
            "来回soyo吃蛋糕": "laihuichidangao_soyo.wav",
            "楞说哈皮": "lengshuohapi.wav",
            "欧内死手": "ouneisishou.wav",
            "欧内的手": "ouneideshou.wav",
            "死人啊灰": "sirenahui.wav",
            "死神狗一拉过来带你哭": "sishengouyilaguolaidainiku.wav",
            "死神环绕＆四象环绕": "sishenhuanraosixianghuanrao.wav",
            "死神的手": "sishendeshou.wav",
            "每年离8次婚": "meinianlicihun_8.wav",
            "每次自己做饭不吃": "meicizijizuofanbuchi.wav",
            "毒火焰": "duhuoyan.wav",
            "水之沙暴": "shuizhishabao.wav",
            "沙扎比": "shazhabi.wav",
            "沙防掩意手": "shafangyanyishou.wav",
            "没有名刀": "meiyoumingdao.wav",
            "海纹十字": "haiwenshizi.wav",
            "深海龙宫": "shenhailonggong.wav",
            "火神医疗功": "huoshenyiliaogong.wav",
            "火龙炎神": "huolongyanshen.wav",
            "热爱海虎我的海虎＆热爱galgame": "reaihaihuwodehaihureai_galgame.wav",
            "熬屎用烟灰撒你": "aoshiyongyanhuisani.wav",
            "爱音soyo": "aiyin_soyo.wav",
            "爷要食大粪": "yeyaoshidafen.wav",
            "牢石耐击术": "laoshinaijishu.wav",
            "独影龙蛇百鹤手": "duyinglongshebaiheshou.wav",
            "猎杀暗黑武神": "lieshaanheiwushen.wav",
            "王亨御剑龙or汉域炎龙": "wanghengyujianlonghanyuyanlong_or.wav",
            "磨刀杀他去": "modaoshataqu.wav",
            "神力大耶稣": "shenlidayesu.wav",
            "神力大龙": "shenlidalong.wav",
            "神力鸭子": "shenliyazi.wav",
            "神威龙神手": "shenweilongshenshou.wav",
            "神秘之矢": "shenmizhishi.wav",
            "红豆": "hongdou.wav",
            "纳米影刀": "namiyingdao.wav",
            "维恩的奥义": "weiendeaoyi.wav",
            "罗汉分身": "luohanfenshen.wav",
            "老姥爷": "laolaoye.wav",
            "老子不要死": "laozibuyaosi.wav",
            "老汉移步": "laohanyibu.wav",
            "耦合": "ouhe.wav",
            "舍不得money": "shebude_money.wav",
            "舍利子回魂": "shelizihuihun.wav",
            "舍利子手": "shelizishou.wav",
            "舍离火涡子手": "shelihuowozishou.wav",
            "若叶睦": "ruoyemu.wav",
            "若叶睦埋尸": "ruoyemumaishi.wav",
            "若叶睦的丝袜迷惑": "ruoyemudesiwamihuo.wav",
            "获得肺炎": "huodefeiyan.wav",
            "蕾影の太快乐了": "leiyingtaikuailele.wav",
            "蛇分身换位影罗万象": "shefenshenhuanweiyingluowanxiang.wav",
            "蛤蟆蛤蟆go": "hamahama_go.wav",
            "蜗牛": "woniu.wav",
            "要让我感恩戴德": "yaorangwoganendaide.wav",
            "谁的手那么香拿来": "sheideshounamexiangnalai.wav",
            "豌豆射手": "wandousheshou.wav",
            "豪兽雷鸣": "haoshouleiming.wav",
            "豪龙国拳": "haolongguoquan.wav",
            "豪龙在天": "haolongzaitian.wav",
            "逆炎立希": "niyanlixi.wav",
            "那是安奈师傅": "nashiannaishifu.wav",
            "都升起来，水都升起来吧": "doushengqilaishuidoushengqilaiba.wav",
            "都回来，都回，都回来": "douhuilaidouhuidouhuilai.wav",
            "都是你之前说的": "doushinizhiqianshuode.wav",
            "释放黑子ikun": "shifangheizi_ikun.wav",
            "闪现袭击你": "shanxianxijini.wav",
            "阎王摆手": "yanwangbaishou.wav",
            "阿妈忒拉斯": "amatelasi.wav",
            "除此之外": "chucizhiwai.wav",
            "韩国影风手": "hanguoyingfengshou.wav",
            "飞天风火轮": "feitianfenghuolun.wav",
            "馒头熟栗子大黑米": "mantoushulizidaheimi.wav",
            "香飘飘热饮": "xiangpiaopiaoreyin.wav",
            "鬼门的手": "guimendeshou.wav",
            "魔影（魔音）": "moyingmoyin.wav",
            "魔骸": "mohai.wav",
            "黑子大炮": "heizidapao.wav",
            "黑暗紊乱升龙": "heianwenluanshenglong.wav",
            "黑鸦魔锻鸦刀": "heiyamoduanyadao.wav",
            "黑龙武神": "heilongwushen.wav",
        }

        # 检查音频文件是否存在
        self._check_audio_files()

    def _check_audio_files(self):
        """检查所有音频文件是否存在"""
        missing_files = []
        for ninjutsu, filename in self.ninjutsu_mapping.items():
            filepath = os.path.join(self.sources_dir, filename)
            if not os.path.exists(filepath):
                missing_files.append(filename)

        if missing_files:
            logger.warning(f"缺少音频文件: {', '.join(missing_files)}")

    @filter.command("释放忍术")
    async def cmd_ninjutsu(self, event: AstrMessageEvent):
        """处理'释放忍术'命令"""
        # 获取用户输入的忍术名称
        ninjutsu_name = event.message_str.replace("/释放忍术", "").strip()

        # 如果没有输入忍术名称
        if not ninjutsu_name:
            yield event.plain_result("杂鱼下忍，连这种忍术都不会释放吗，杂鱼杂鱼")
            return

        # 藏经阁特殊功能
        if ninjutsu_name == "藏经阁":
            ninjutsu_list = ["📜 忍术藏经阁 📜",
                             "记载的所有忍术如下："]
            ninjutsu_list.extend([f"· {name}" for name in self.ninjutsu_mapping.keys()])
            yield event.plain_result("\n".join(ninjutsu_list))
            return

        # 检查输入的忍术是否存在
        if ninjutsu_name not in self.ninjutsu_mapping:
            yield event.plain_result("杂鱼下忍，连这种程度的忍术都要我帮你释放吗，杂鱼杂鱼")
            return

        # 获取对应的音频文件路径
        audio_file = os.path.join(self.sources_dir, self.ninjutsu_mapping[ninjutsu_name])

        # 检查文件是否存在
        if not os.path.exists(audio_file):
            yield event.plain_result(f"忍术 {ninjutsu_name} 的音频文件丢失了!")
            return

        # 发送语音消息
        try:
            from astrbot.api.message_components import Record
            yield event.chain_result([
                event.plain_result(f"{event.sender_nickname} 释放了「{ninjutsu_name}」!"),
                Record(file=audio_file)
            ])
        except Exception as e:
            logger.error(f"发送语音失败: {str(e)}")
            yield event.plain_result("释放忍术失败，查克拉不足!")