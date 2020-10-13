import speedtest
import logging




class SpeedTest:

    def run_speedtest(self):
        print ('Sure! Running a speed test. Wait a second to measure!')
        try:
            st = speedtest.Speedtest()
            server_names = []
            st.get_servers(server_names)

            downlink_bps = st.download()
            uplink_bps = st.upload()
            ping = st.results.ping
            up_mbps = uplink_bps / 1000000
            down_mbps = downlink_bps / 1000000

            print("Speedtest results:\n"
                         "The ping is: %s ms \n"
                         "The upling is: %0.2f Mbps \n"
                         "The downling is: %0.2f Mbps" % (ping, up_mbps, down_mbps)
                         )

        except Exception as e:
            print("I coudn't run a speedtest")
            logging.error("Speedtest error with message: {0}".format(e))


#st = SpeedTest()
#st.run_speedtest()
