import os
from typing import Optional, Tuple

from PySide6.QtGui import QIcon
from qfluentwidgets import FluentIcon, FluentThemeColor

from one_dragon.envs.env_config import DEFAULT_GIT_PATH, EnvConfig, env_config
from one_dragon.envs.git_service import git_service, GitService
from one_dragon.envs.project_config import ProjectConfig, project_config
from one_dragon.gui.install_card.wtih_existed_install_card import WithExistedInstallCard
from one_dragon.utils.i18_utils import gt


class GitInstallCard(WithExistedInstallCard):

    def __init__(self):
        self.env_config: EnvConfig = env_config
        self.project_config: ProjectConfig = project_config
        self.git_service: GitService = git_service

        super().__init__(title_cn='Git',
                         install_method=self.git_service.install_default_git,
                         )

    def get_existed_os_path(self) -> Optional[str]:
        """
        获取系统环境变量中的路径，由子类自行实现
        :return:
        """
        return self.git_service.get_os_git_path()

    def on_existed_chosen(self, file_path: str) -> None:
        """
        选择了本地文件之后的回调，由子类自行实现
        :param file_path: 本地文件的路径
        :return:
        """
        self.env_config.git_path = file_path
        super().on_existed_chosen(file_path)

    def after_progress_done(self, success: bool) -> None:
        """
        安装结束的回调，由子类自行实现
        :param success:
        :return:
        """
        if success:
            self.env_config.git_path = DEFAULT_GIT_PATH
            self.check_and_update_display()
        else:
            self.update_display(FluentIcon.INFO.icon(color=FluentThemeColor.RED.value), gt('安装失败', 'ui'))

    def get_display_content(self) -> Tuple[QIcon, str]:
        """
        获取需要显示的状态，由子类自行实现
        :return: 显示的图标、文本
        """
        git_path = self.env_config.git_path

        if git_path == '':
            icon = FluentIcon.INFO.icon(color=FluentThemeColor.RED.value)
            msg = gt('未安装', 'ui')
        elif not os.path.exists(git_path):
            icon = FluentIcon.INFO.icon(color=FluentThemeColor.RED.value)
            msg = gt('文件不存在', 'ui')
        else:
            git_version = self.git_service.get_git_version()
            if git_version is None:
                icon = FluentIcon.INFO.icon(color=FluentThemeColor.RED.value)
                msg = gt('无法获取Git版本', 'ui') + ' ' + git_path
            else:
                icon = FluentIcon.INFO.icon(color=FluentThemeColor.DEFAULT_BLUE.value)
                msg = f"{gt('已安装', 'ui')}" + ' ' + git_path

        return icon, msg
