#!/usr/bin/python

import os
import subprocess

class DECISION:
    KEEP = 1
    CHANGE = 2

class Wizard:
    def run(self):
        try:
            self.greet_hello()

            self.configure_environment()
            self.configure_cli_shortcuts()
            self.configure_ssh()

            self.say_goodbye()

        except KeyboardInterrupt:
            self.print_abortion_prompt()

        self.print_end_disclaimer()

    def configure_environment(self):
        self.configure_user_name()
        self.configure_user_email()
        GitConfig().configure_global_git_settings()

    def configure_ssh(self):
        if self.ask_if_user_wants_to_setup_ssh_key() == False:
            return

        sshConfig = SshConfig()
        self.print_ssh_keygen_instructions()
        sshConfig.generate_ssh_keys()
        self.print_public_ssh_key_with_instructions(sshConfig.get_public_ssh_key())

    def configure_cli_shortcuts(self):
        pass

    def greet_hello(self):
        print(
        "\nWelcome %s. This script will help you setup your GitHub account on this computer :)\n" % os.environ["USER"])

    def say_goodbye(self, aborted = False):
        print("\nYou're all set :)")
        print("Make sure to checkout repositories only with SSH links from GitHub.")
        print("It's been a pleasure setting up your git.\n")

    def print_abortion_prompt(self):
        print("\n\n=============================  ABORTED  =============================")

    def print_end_disclaimer(self):
        print("* You can always run this script again to configure your git settings\n")

    def configure_user_name(self):
        gitConfig = GitConfig()
        current_username = gitConfig.get_user_name()
        new_username = self.prompt_user_for_value("Please enter your full name", current_username)
        if new_username != current_username:
            gitConfig.configure_user_name(new_username)

    def configure_user_email(self):
        gitConfig = GitConfig()
        current_user_email = gitConfig.get_user_email()
        new_user_email = self.prompt_user_for_value("Please enter your GitHub user email", current_user_email)
        if new_user_email != current_user_email:
            gitConfig.configure_user_email(current_user_email)

    def prompt_user_for_value(self, prompt, current_value):
        if current_value != '':
            prompt = "%s%s" % (prompt, " [%s]" % current_value)
        prompt = "%s%s" % (prompt, ": ")
        user_input = raw_input("%s" % prompt).strip()
        if user_input == '':
            return current_value
        return user_input

    def ask_if_user_wants_to_setup_ssh_key(self):
        return raw_input("Would you like to generate an SSH key? [Y/n]: ") != 'n'

    def print_ssh_keygen_instructions(self):
        print('')
        print("** When prompted to enter a file path to save your SSH key just click Enter.")
        print("** When prompted for a passphrase, it's not the your user password. You can leave it empty, but make sure to remember the passphrase if you wish to set it.")

    def print_public_ssh_key_with_instructions(self, public_ssh_key):
        print("\n==========================================================================")
        print("Follow instructions to complete ssh connection:")
        print("Copy the key below (everything between the triple quotes) and go to to the link: https://github.com/settings/keys\n")
        print("\"\"\"")
        print("%s" % public_ssh_key)
        print("\"\"\"\n")
        print("There click the 'New SSH key' button and paste it in the designated text field.")
        print("The Title requested is just for tracking. You can enter 'Work Desktop'.")


class GitConfig:
    def get_user_name(self):
        try:
            return subprocess.check_output(['git', 'config', 'user.name']).strip()
        except subprocess.CalledProcessError:
            return ''

    def configure_user_name(self, username):
        subprocess.call(['git', 'config', '--global', 'user.name', '%s' % username])

    def get_user_email(self):
        try:
            return subprocess.check_output(['git', 'config', 'user.email']).strip()
        except subprocess.CalledProcessError:
            return ''

    def configure_user_email(self, user_email):
        subprocess.call(['git', 'config', '--global', 'user.email', "%s" % user_email])
        pass

    def configure_global_git_settings(self):
        subprocess.call(['git', 'config', '--global', ',push.default', 'simple'])


class SshConfig():
    def get_public_ssh_key(self):
        public_ssh_file = open(os.path.join(os.sep, 'home', os.environ['USER'], '.ssh', 'id_rsa.pub'))
        return '\n'.join(public_ssh_file.readlines())

    def generate_ssh_keys(self):
        subprocess.call(['ssh-keygen', '-t', 'rsa', '-b', '4096', '-C', '%s' % GitConfig().get_user_email()])


if __name__ == "__main__":
    Wizard().run()