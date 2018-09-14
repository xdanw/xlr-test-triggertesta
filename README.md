# XL Release Description

## Overview

This hotfix adds support for Sonatype Nexus v3 servers.

## Installing

There are currently two ways to install: as a replacement or as a separate plugin.

This version is intended to be backwards compatible: outputs and code were added, but no existing ones were removed. However, as with all plugins, downgrading any plugin can cause issues after a release has been created. Therefore, this can also be installed a separate plugin, which eliminates the risk of affecting Nexus V2 integrations. You'll just need to retype any server logins.

## Install as Patch

To install as a *hotfix*, which will replace your existing plugin, move the existing xlr-nexus3-releasetrigger-1.0.0.jar out of the plugins/xlr-official directory. Then copy the included .jar file into either the __local__ or the xlr-official directory. Once installed, you'll select the "Server V3" checkbox on any triggers that use a v3 server.

## Install as new plugin

To install as a *separate plugin*, go to the Nexus3_Separate_Plugin folder and either copy the .jar file into plugins/__local__, or copy the contents into /ext taking care to merge and NOT replace synthetic.xml. Once installed, you'll have "Nexus3" as a new server type and trigger type.
