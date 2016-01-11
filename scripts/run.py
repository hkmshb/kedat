"""
Script Runner.
"""
import network

run = network.run


if __name__ == '__main__':
    run(network.clear_kedco_db)
    run(network.Loader._loadMV_network_stations_feeders)
    run(network.Loader._loadLV_network_stations)
    #run(network.reorder_distss)
    print('done')
    