from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget
from qfluentwidgets import FluentIcon, SettingCardGroup, setTheme, Theme, VBoxLayout

from one_dragon.base.config.config_item import get_config_item_from_enum
from one_dragon.base.operation.context_base import OneDragonContext
from one_dragon.envs.env_config import RepositoryTypeEnum, GitMethodEnum, ProxyTypeEnum, ThemeEnum
from one_dragon.gui.component.interface.vertical_scroll_interface import VerticalScrollInterface
from one_dragon.gui.component.setting_card.combo_box_setting_card import ComboBoxSettingCard
from one_dragon.gui.component.setting_card.key_setting_card import KeySettingCard
from one_dragon.gui.component.setting_card.switch_setting_card import SwitchSettingCard
from one_dragon.gui.component.setting_card.text_setting_card import TextSettingCard
from one_dragon.utils.i18_utils import gt


class SettingEnvInterface(VerticalScrollInterface):

    def __init__(self, ctx: OneDragonContext, parent=None):
        self.ctx: OneDragonContext = ctx

        content_widget = QWidget()
        content_layout = VBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        content_layout.addWidget(self._init_basic_group())
        content_layout.addWidget(self._init_git_group())
        content_layout.addWidget(self._init_web_group())
        content_layout.addWidget(self._init_key_group())

        VerticalScrollInterface.__init__(
            self,
            ctx=ctx,
            object_name='setting_env_interface',
            content_widget=content_widget, parent=parent,
            nav_text_cn='脚本环境'
        )

    def _init_basic_group(self) -> SettingCardGroup:
        basic_group = SettingCardGroup(gt('基础', 'ui'))

        self.theme_opt = ComboBoxSettingCard(
            icon=FluentIcon.CONSTRACT, title='界面主题', content='有没有大神提供个好配色',
            options=ThemeEnum
        )
        self.theme_opt.value_changed.connect(self._on_theme_changed)
        basic_group.addSettingCard(self.theme_opt)

        self.debug_opt = SwitchSettingCard(
            icon=FluentIcon.SEARCH, title='调试模式', content='正常无需开启'
        )
        self.debug_opt.value_changed.connect(self._on_debug_changed)
        basic_group.addSettingCard(self.debug_opt)

        return basic_group

    def _init_git_group(self) -> SettingCardGroup:
        git_group = SettingCardGroup(gt('Git相关', 'ui'))

        self.repository_type_opt = ComboBoxSettingCard(
            icon=FluentIcon.APPLICATION, title='代码源', content='国内无法访问Github则选择Gitee',
            options=RepositoryTypeEnum
        )
        self.repository_type_opt.value_changed.connect(self._on_repo_type_changed)
        git_group.addSettingCard(self.repository_type_opt)

        self.git_method_opt = ComboBoxSettingCard(
            icon=FluentIcon.SYNC, title='拉取方式', content='不懂什么是ssh就选https',
            options=GitMethodEnum
        )
        self.git_method_opt.value_changed.connect(self._on_git_method_changed)
        git_group.addSettingCard(self.git_method_opt)

        return git_group

    def _init_web_group(self) -> SettingCardGroup:
        web_group = SettingCardGroup(gt('网络相关', 'ui'))

        self.proxy_type_opt = ComboBoxSettingCard(
            icon=FluentIcon.GLOBE, title='网络代理', content='免费代理仅能加速工具和模型下载，无法加速代码同步',
            options=ProxyTypeEnum
        )
        self.proxy_type_opt.value_changed.connect(self._on_proxy_type_changed)
        web_group.addSettingCard(self.proxy_type_opt)

        self.personal_proxy_input = TextSettingCard(
            icon=FluentIcon.WIFI, title='个人代理', content='网络代理中选择 个人代理 后生效',
            input_placeholder='http://127.0.0.1:8080'
        )
        self.personal_proxy_input.value_changed.connect(self._on_personal_proxy_changed)
        web_group.addSettingCard(self.personal_proxy_input)

        return web_group

    def _init_key_group(self) -> SettingCardGroup:
        key_group = SettingCardGroup(gt('脚本按键', 'ui'))

        self.key_start_running_input = KeySettingCard(
            icon=FluentIcon.PLAY, title='开始运行', content='开始、暂停、恢复某个应用',
        )
        self.key_start_running_input.value_changed.connect(self._on_key_start_running_changed)
        key_group.addSettingCard(self.key_start_running_input)

        self.key_stop_running_input = KeySettingCard(
            icon=FluentIcon.CLOSE, title='停止运行', content='停止正在运行的应用，不能恢复'
        )
        self.key_stop_running_input.value_changed.connect(self._on_key_stop_running_changed)
        key_group.addSettingCard(self.key_stop_running_input)

        self.key_screenshot_input = KeySettingCard(
            icon=FluentIcon.CAMERA, title='游戏截图', content='用于开发、提交bug。会自动对UID打码，保存在 .debug/images/ 文件夹中'
        )
        self.key_screenshot_input.value_changed.connect(self._on_key_screenshot_changed)
        key_group.addSettingCard(self.key_screenshot_input)

        self.key_mouse_pos_input = KeySettingCard(
            icon=FluentIcon.MOVE, title='鼠标位置', content='日志中输出当前鼠标位置，用于开发'
        )
        self.key_mouse_pos_input.value_changed.connect(self._on_key_mouse_position_changed)
        key_group.addSettingCard(self.key_mouse_pos_input)

        return key_group

    def init_on_shown(self) -> None:
        """
        子界面显示时 进行初始化
        :return:
        """
        theme = get_config_item_from_enum(ThemeEnum, self.ctx.env_config.theme)
        if theme is not None:
            self.theme_opt.setValue(theme.value)

        self.debug_opt.setValue(self.ctx.env_config.is_debug)

        self.key_start_running_input.setValue(self.ctx.env_config.key_start_running)
        self.key_stop_running_input.setValue(self.ctx.env_config.key_stop_running)
        self.key_screenshot_input.setValue(self.ctx.env_config.key_screenshot)
        self.key_mouse_pos_input.setValue(self.ctx.env_config.key_mouse_pos)

        repo_type = get_config_item_from_enum(RepositoryTypeEnum, self.ctx.env_config.repository_type)
        if repo_type is not None:
            self.repository_type_opt.setValue(repo_type.value)

        git_method = get_config_item_from_enum(GitMethodEnum, self.ctx.env_config.git_method)
        if git_method is not None:
            self.git_method_opt.setValue(git_method.value)

        proxy_type = get_config_item_from_enum(ProxyTypeEnum, self.ctx.env_config.proxy_type)
        if proxy_type is not None:
            self.proxy_type_opt.setValue(proxy_type.value)

        self.personal_proxy_input.setValue(self.ctx.env_config.personal_proxy)

    def _on_theme_changed(self, index: int, value: str) -> None:
        """
        仓库类型改变
        :param index: 选项下标
        :param value: 值
        :return:
        """
        config_item = get_config_item_from_enum(ThemeEnum, value)
        self.ctx.env_config.theme = config_item.value
        setTheme(Theme[config_item.value.upper()])

    def _on_debug_changed(self, value: bool):
        """
        调试模式改变
        :param value:
        :return:
        """
        self.ctx.env_config.is_debug = value
        self.ctx.init_by_config()

    def _on_repo_type_changed(self, index: int, value: str) -> None:
        """
        仓库类型改变
        :param index: 选项下标
        :param value: 值
        :return:
        """
        config_item = get_config_item_from_enum(RepositoryTypeEnum, value)
        self.ctx.env_config.repository_type = config_item.value

    def _on_git_method_changed(self, index: int, value: str) -> None:
        """
        拉取方式改变
        :param index: 选项下标
        :param value: 值
        :return:
        """
        config_item = get_config_item_from_enum(GitMethodEnum, value)
        self.ctx.env_config.git_method = config_item.value

    def _on_proxy_type_changed(self, index: int, value: str) -> None:
        """
        拉取方式改变
        :param index: 选项下标
        :param value: 值
        :return:
        """
        config_item = get_config_item_from_enum(ProxyTypeEnum, value)
        self.ctx.env_config.proxy_type = config_item.value
        self._on_proxy_changed()

    def _on_personal_proxy_changed(self, value: str) -> None:
        """
        个人代理改变
        :param value: 值
        :return:
        """
        self.ctx.env_config.personal_proxy = value
        self._on_proxy_changed()

    def _on_proxy_changed(self) -> None:
        """
        代理发生改变
        :return:
        """
        self.ctx.git_service.is_proxy_set = False

    def _on_key_start_running_changed(self, value: str) -> None:
        self.ctx.env_config.key_start_running = value

    def _on_key_stop_running_changed(self, value: str) -> None:
        self.ctx.env_config.key_stop_running = value

    def _on_key_screenshot_changed(self, value: str) -> None:
        self.ctx.env_config.key_screenshot = value

    def _on_key_mouse_position_changed(self, value: str) -> None:
        self.ctx.env_config.key_mouse_pos = value