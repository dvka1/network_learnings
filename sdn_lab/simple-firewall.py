from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3

class SimpleFirewall(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    # Runs once when a switch connects (handshake / features message)
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        dp = ev.msg.datapath                # "datapath" = object representing the switch
        ofp = dp.ofproto                    # constants for OpenFlow (ports, etc.)
        parser = dp.ofproto_parser          # helper to build matches/actions/FlowMod

        # 1) DROP rule: match IPv4 packets from 10.0.0.1 -> 10.0.0.2 (ICMP and TCP both matched here)
        # Note: eth_type=0x0800 ensures it's IPv4
        match = parser.OFPMatch(ipv4_src="10.0.0.1", ipv4_dst="10.0.0.2", eth_type=0x0800)
        # create FlowMod with NO instructions -> switch treats this as "install rule with no actions" => drop
        dp.send_msg(parser.OFPFlowMod(datapath=dp, priority=100, match=match, instructions=[]))

        # 2) DEFAULT rule: everything else -> OFPP_NORMAL (let OVS do normal L2 switching)
        actions = [parser.OFPActionOutput(ofp.OFPP_NORMAL)]
        inst = [parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]
        dp.send_msg(parser.OFPFlowMod(datapath=dp, priority=1, match=parser.OFPMatch(), instructions=inst))

