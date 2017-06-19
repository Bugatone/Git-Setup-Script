#!/usr/bin/python

import os
import subprocess

class DECISION:
    KEEP = 1
    CHANGE = 2

class Wizard:
    def greet_hello(self):
        print(
        "\nWelcome %s. This script will help you setup your GitHub account on this computer :)\n" % os.environ["USER"])

    def say_goodbye(self, aborted = False):
        if aborted:
            print("\n\n===  ABORTED  ===")
        else:
            print("\nYou're all set :)")
            print("Make sure to checkout repositories only with SSH links from GitHub.")
            print("It's been a pleasure setting up your git.\n")
        print("* You can always run this script again to configure your git settings\n")

    def ask_if_user_wants_to_keep_current_email(self, email):
        print("Your email is currently configured to '%s'." % email)
        if raw_input("Would you like to keep it? [Y/n]: ") == 'n':
            return DECISION.CHANGE
        return DECISION.KEEP

    def ask_if_user_wants_to_keep_current_name(self, name):
        print("Your name is currently configured to '%s'." % name)
        if raw_input("Would you like to keep it? [Y/n]: ") == 'n':
            return DECISION.CHANGE
        return DECISION.KEEP

    def ask_user_for_name(self):
        return raw_input("Please enter your full name: ").strip()

    def ask_user_for_email(self):
        return raw_input("Please enter your GitHub user email: ").strip()

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

    def is_user_name_configured(self):
        return self.get_user_name() != ''

    def configure_user_name(self, withWizard):
        wizard = withWizard
        user_name = wizard.ask_user_for_name()
        subprocess.call(['git', 'config', '--global', 'user.name', '%s' % user_name])

    def get_user_email(self):
        try:
            return subprocess.check_output(['git', 'config', 'user.email']).strip()
        except subprocess.CalledProcessError:
            return ''

    def is_user_email_configured(self):
        return self.get_user_email() != ''

    def configure_user_email(self, withWizard):
        wizard = withWizard
        user_email = wizard.ask_user_for_email()
        subprocess.call(['git', 'config', '--global', 'user.email', "%s" % user_email])
        pass

    def configure_ssh(self, withWizard):
        wizard = withWizard
        wizard.print_ssh_keygen_instructions()
        self._generate_ssh_keys()
        public_ssh_key = self._get_public_ssh_key()
        wizard.print_public_ssh_key_with_instructions(public_ssh_key)

    def configure_global_git_settings(self):
        subprocess.call(['git', 'config', '--global', ',push.default', 'simple'])

    def _generate_ssh_keys(self):
        subprocess.call(['ssh-keygen', '-t', 'rsa', '-b', '4096', '-C', '%s' % self.get_user_email()])

    def _get_public_ssh_key(self):
        public_ssh_file = open(os.path.join(os.sep, 'home', os.environ['USER'], '.ssh', 'id_rsa.pub'))
        return '\n'.join(public_ssh_file.readlines())


if __name__ == "__main__":
    wizard = Wizard()
    try:
        wizard.greet_hello()

        gitConfig = GitConfig()

        if not gitConfig.is_user_name_configured():
            gitConfig.configure_user_name(withWizard=wizard)
        else:
            if wizard.ask_if_user_wants_to_keep_current_name(gitConfig.get_user_name()) == DECISION.CHANGE:
                gitConfig.configure_user_name(withWizard=wizard)

        if not gitConfig.is_user_email_configured():
            gitConfig.configure_user_email(withWizard=wizard)
        else:
            if wizard.ask_if_user_wants_to_keep_current_email(gitConfig.get_user_email()) == DECISION.CHANGE:
                gitConfig.configure_user_email(withWizard=wizard)

        gitConfig.configure_global_git_settings()

        if wizard.ask_if_user_wants_to_setup_ssh_key():
            gitConfig.configure_ssh(withWizard=wizard)

        wizard.say_goodbye()

    except KeyboardInterrupt:
        wizard.say_goodbye(aborted=True)