[33mcommit f099bce[m
Author: Tommy <thomas.milox@epitech.eu>
Date:   Thu Jul 6 22:55:51 2017 +0200

    Added check if an user call a plugin without giving a command

[33mcommit 30faec7[m
Author: Tommy <thomas.milox@epitech.eu>
Date:   Thu Jul 6 01:51:56 2017 +0200

    removed unused import & fix typo

[33mcommit 8e4526a[m
Author: Tommy <thomas.milox@epitech.eu>
Date:   Thu Jul 6 01:49:56 2017 +0200

    need to fix the communication through the pipe

[33mcommit 20231a3[m
Author: Tommy <thomas.milox@epitech.eu>
Date:   Wed Jul 5 17:13:46 2017 +0200

    keep working on plugin execution

[33mcommit af70c2e[m
Author: Tommy <thomas.milox@epitech.eu>
Date:   Tue Jul 4 12:59:37 2017 +0200

    Update PluginStore according comments on commit: 1d296af
    Removed useless print for debug.
    Replace docstrings according PEP 257: docstring conventions

[33mcommit 1d296af[m
Author: Tommy <thomas.milox@epitech.eu>
Date:   Tue Jul 4 00:11:19 2017 +0200

    Dedicated process for the plugins are spawned and stored correctly

[33mcommit 9ed557c[m
Author: Tommy <thomas.milox@epitech.eu>
Date:   Mon Jul 3 19:14:08 2017 +0200

    starting implementation of plugin process

[33mcommit 627fbcb[m
Author: Tommy <thomas.milox@epitech.eu>
Date:   Sun Jul 2 14:50:56 2017 +0200

    initial commit on plugin_exec

[33mcommit 1c16c1f[m
Author: Tommy <thomas.milox@epitech.eu>
Date:   Sun Jul 2 14:46:52 2017 +0200

    fix input

[33mcommit 45063c0[m
Author: Tommy <thomas.milox@epitech.eu>
Date:   Sun Jul 2 14:36:06 2017 +0200

    remove pocketsphinx until fix import

[33mcommit 98ccf5c[m
Author: Dorian Amouroux <dor.amouroux@gmail.com>
Date:   Sun Jul 2 12:35:43 2017 +0200

    fix audio input

[33mcommit aea01e2[m
Merge: bb082fa de1b348
Author: Dorian Amouroux <dor.amouroux@gmail.com>
Date:   Sun Jul 2 12:06:03 2017 +0200

    Merge pull request #2 from ava-project/plugins_manager
    
    Update plugins

[33mcommit de1b348[m
Merge: a0b92e8 bb082fa
Author: Dorian Amouroux <dor.amouroux@gmail.com>
Date:   Sun Jul 2 12:02:49 2017 +0200

    Merge branch 'master' into plugins_manager

[33mcommit a0b92e8[m
Author: Tommy <thomas.milox@epitech.eu>
Date:   Sun Jul 2 04:04:27 2017 +0200

    removed useless import

[33mcommit 11e0c90[m
Author: Tommy <thomas.milox@epitech.eu>
Date:   Sun Jul 2 03:59:15 2017 +0200

    fix typo

[33mcommit ce7fc04[m
Author: Tommy <thomas.milox@epitech.eu>
Date:   Sun Jul 2 03:23:44 2017 +0200

    Export loading of a plugin, rework of PluginManager and PluginStore

[33mcommit bb082fa[m
Author: Guiz <guillaume.briard@epitech.eu>
Date:   Sun Jul 2 02:44:57 2017 +0200

    Speech To Text basic behavior

[33mcommit 62c7139[m
Author: Guiz <guillaume.briard@epitech.eu>
Date:   Sat Jul 1 23:15:58 2017 +0200

    update README regarding Speech to Text component

[33mcommit 1230f7b[m
Author: Guiz <guillaume.briard@epitech.eu>
Date:   Sat Jul 1 23:00:49 2017 +0200

    audio_input component removed

[33mcommit 92361b7[m
Author: Tommy <thomas.milox@epitech.eu>
Date:   Sat Jul 1 22:11:41 2017 +0200

    Implemented plugin builtins

[33mcommit b4a428a[m
Author: Guiz <guillaume.briard@epitech.eu>
Date:   Sat Jul 1 19:22:45 2017 +0200

    STT (done) / TTS (to work) engines class

[33mcommit 53486af[m
Author: Guiz <guillaume.briard@epitech.eu>
Date:   Sat Jul 1 18:33:08 2017 +0200

    RawInput class for audio_input component

[33mcommit 1164346[m
Author: Tommy <thomas.milox@epitech.eu>
Date:   Sat Jul 1 17:51:31 2017 +0200

    update architecture

[33mcommit 8ecb5d0[m
Author: Dorian Amouroux <dor.amouroux@gmail.com>
Date:   Sat Jul 1 17:38:45 2017 +0200

    Update README.md

[33mcommit b746858[m
Author: Tommy <thomas.milox@epitech.eu>
Date:   Sat Jul 1 17:10:48 2017 +0200

    Starting implementation of plugin_manager, plugin_runner, plugin_store

[33mcommit dba2269[m
Author: Dorian Amouroux <dor.amouroux@gmail.com>
Date:   Sat Jul 1 15:51:07 2017 +0200

    setup method in component

[33mcommit 332c0df[m
Author: Dorian Amouroux <dor.amouroux@gmail.com>
Date:   Sat Jul 1 15:50:37 2017 +0200

    handling end of file exception

[33mcommit 4b507d2[m
Author: Tommy <thomas.milox@epitech.eu>
Date:   Fri Jun 30 21:32:02 2017 +0200

    PluginsManager: implemented parsing plugins folders, caching data, install and uninstall features

[33mcommit 26c8c79[m
Author: Dorian Amouroux <dor.amouroux@gmail.com>
Date:   Fri Jun 30 15:05:21 2017 +0200

    infinite loop in the component manager

[33mcommit 06714e0[m
Merge: 2c1f77a 0742cf5
Author: Dorian Amouroux <dor.amouroux@gmail.com>
Date:   Fri Jun 30 14:57:08 2017 +0200

    Merge branch 'master' of github.com:ava-project/AVA

[33mcommit 2c1f77a[m
Author: Dorian Amouroux <dor.amouroux@gmail.com>
Date:   Fri Jun 30 14:56:55 2017 +0200

    handling CTRL C

[33mcommit 0742cf5[m
Author: Dorian Amouroux <dor.amouroux@gmail.com>
Date:   Fri Jun 30 14:38:55 2017 +0200

    Update README.md

[33mcommit ead81f7[m
Author: Dorian Amouroux <dor.amouroux@gmail.com>
Date:   Fri Jun 30 14:25:22 2017 +0200

    daemonized threads

[33mcommit 3bc117a[m
Author: Dorian Amouroux <dor.amouroux@gmail.com>
Date:   Fri Jun 30 13:32:38 2017 +0200

    component in init in the thread

[33mcommit c25c92e[m
Author: Dorian Amouroux <dor.amouroux@gmail.com>
Date:   Fri Jun 30 13:31:50 2017 +0200

    refactor component starting up

[33mcommit 38bdac6[m
Author: Dorian Amouroux <dor.amouroux@gmail.com>
Date:   Fri Jun 30 12:33:18 2017 +0200

    use queue singleton

[33mcommit eb7ccdb[m
Author: Dorian Amouroux <dor.amouroux@gmail.com>
Date:   Fri Jun 30 11:42:55 2017 +0200

    all the execution flow

[33mcommit 4e1cd32[m
Author: Dorian Amouroux <dor.amouroux@gmail.com>
Date:   Fri Jun 30 10:36:22 2017 +0200

    create all queues as singleton

[33mcommit ad1cba4[m
Author: Dorian Amouroux <dor.amouroux@gmail.com>
Date:   Fri Jun 30 10:06:42 2017 +0200

    boilerplate daemon

[33mcommit 92412d4[m
Author: Dorian Amouroux <dor.amouroux@gmail.com>
Date:   Fri Jun 30 10:00:06 2017 +0200

    Initial commit
