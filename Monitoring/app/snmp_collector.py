from pysnmp.entity import engine, config
from pysnmp.hlapi.asyncio import UdpTransportTarget, sendNotification, ContextData
from pysnmp.entity.rfc3413.oneliner import ntforg

async def send_snmp_trap():
    # Configurer les paramètres du périphérique SNMP
    target_host = '192.168.1.1'  # Remplacez par l'adresse IP de votre périphérique SNMP activé
    community = 'public'  # Remplacez par la communauté SNMP correcte

    # Configurer le serveur SNMP Traps
    trap_receiver = UdpTransportTarget(('0.0.0.0', 162))

    # Configurer le gestionnaire SNMP
    snmp_engine = engine.SnmpEngine()
    config.addTransport(
    snmp_engine,
   UdpTransportTarget(('0.0.0.0', 161)).openClientMode()

)

    config.addV3User(
        snmp_engine, 'my-user',
        config.usmHMACMD5AuthProtocol, 'authkey1',
        config.usmAesCfb128Protocol, 'privkey1'
    )
    config.addTargetParams(snmp_engine, 'my-creds', 'my-user', 'authNoPriv')
    config.addTargetAddr(
        snmp_engine, 'my-router', 
        UdpTransportTarget(('192.168.1.1', 161)),
        'my-creds', 'authNoPriv'
    )

    # Configurer le gestionnaire de notifications
    ntforg.NotificationReceiver(snmp_engine, lambda x: print(f"Notification: {x.prettyPrint()}"))
    contextData = ntforg.ContextData()

    # Envoyer un trap SNMP
    error_indication, error_status, error_index, var_binds = await next(
        sendNotification(
            snmp_engine,
            UdpTransportTarget(('192.168.1.1', 162)),
            contextData=contextData,
        )
    )

    if error_indication:
        print(f"Error sending SNMP trap: {error_indication}")
    else:
        print(f"SNMP trap sent successfully")

    # Arrêter le gestionnaire SNMP
    snmp_engine.transportDispatcher.closeDispatcher()

# Utiliser asyncio pour exécuter la fonction asynchrone
import asyncio
loop = asyncio.get_event_loop()
loop.run_until_complete(send_snmp_trap())
