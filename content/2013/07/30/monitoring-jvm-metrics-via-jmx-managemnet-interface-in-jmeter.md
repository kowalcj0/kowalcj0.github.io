---
title: Monitoring JVM metrics via JMX management interface in JMeter
description: 
date: 2013-07-30T14:31:45
slug: monitoring-jvm-metrics-via-jmx-management-interface-in-jmeter
draft: false
categories:
  - wordpress
  - testing
tags:
  - java
  - jmeter
---

What do we need: 

* any java application (doesn't matter whether it was written in Java/Play/Groovy/JPython etc)
* [PerfMon Server Agent](https://github.com/undera/perfmon-agent)
* [Apache JMeter](https://jmeter.apache.org/) wiith [jmeter-plugins](https://jmeter-plugins.org/) installed


Once you have plugins installed them in the jMeter's `lib/ext` folder, then: 

1. On the box you want to monitor, copy templates: `jmxremote.password` & `jmxremote.access` from `$JAVA_HOME/lib/management` to for example: `/srv/play/`
2. edit them according to your liking 
3. launch your JAVA application with additional parameters: 
    ```bash
    java \
        -jar your_application.jar \
        -Dcom.sun.management.jmxremote \
        -Dcom.sun.management.jmxremote.ssl=false \
        -Dcom.sun.management.jmxremote.authenticate=false \
        -Dcom.sun.management.jmxremote.port=10006 \
        -Dcom.sun.management.jmxremote.password.file=/srv/play/jmxremote.password \
        -Dcom.sun.management.jmxremote.access.file=/srv/play/jmxremote.access
    ```
4. start a server-agent (http://jmeter-plugins.org/wiki/PerfMonAgent/) on the host which JVM metrics you want to monitor using command like: 
    ```bash
    cd ${jmeter_folder}/lib/ext/
    java \
       -jar ./CMDRunner.jar \
       --tool PerfMonAgent \
       --udp-port 0 \
       --tcp-port 7777
    ```
    You can also run it as background process and detach from your session, so it will continue to work even if you disconnect from the server. 
    ```bash
    cd ${jmeter_folder}/lib/ext/
    nohup java \
       -jar ./CMDRunner.jar \
       --tool PerfMonAgent \
       --udp-port 0 \
       --tcp-port 7777 &
    ```
5. add "`PerfMon Metrics Collector`" to your test plan
6. provide the hostname/IP address of the box running server-agent in the "`Host/IP`" field (don't forget about the port :) )
7. select JMX as the "`Metric to collect`"
8. double click on "`Metric parameter`" field and then click on the "`...`" button to the right
9. enter all the credentials that the server-agent will use to connect to the local JVM via JMX port. Here's an example config: 
    ```bash
    url=localhost\:10006:user=role:password=password:gc-time
    ```
    Where role & password are of course defined in the `jmxremote.password` & `jmxremote.access` files 

btw. Here's an {{< download href="../drKingShultz.jmx" title="example test plan" >}} with preconfigured PerfMon listener.  
If everything was configured properly the you should see something like that on the PerfMon graph: 


{{< figure src="../example_jmx_metrics.png" title="An example PerfMon graph with JVM Metrics" >}}
