#! /usr/bin/env ruby

require 'orocos'
require 'orocos/log'
require 'rock/bundle'
require 'vizkit'

include Orocos

Bundles.initialize

# This ruby scripts takes the interlaced bb2 frame and saves the deinterlaced pairs in a new log file

Orocos.run 'camera_bb2::Task' => 'camera_bb2' do
    
    # Declare logger of new ports
    logger_bb2 = Orocos.name_service.get 'camera_bb2_Logger'
    
    # New log destination
    logger_bb2.file = "bb2_deinterlaced.log"
    
    # New components to run on top of the log
    camera_bb2 = Orocos.name_service.get 'camera_bb2'
    Orocos.conf.apply(camera_bb2, ['default'], :override => true)
 
    # Open log file to be postprocessed
    if ARGV.size == 0 then
		log_replay = Orocos::Log::Replay.open("bb2.log")
    else
		log_replay = Orocos::Log::Replay.open(ARGV[0] + "bb2.log")
    end
    
    # Uses timestamp when data was acquired
    log_replay.use_sample_time = true
    
    # New connection (either to logfed ports or new components
    log_replay.camera_firewire_bb2.frame.connect_to(camera_bb2.frame_in)
        
    # Data to be logged
    logger_bb2.log(camera_bb2.left_frame)
    logger_bb2.log(camera_bb2.right_frame)
    #logger_bb2.log(camera_bb2.right_frame.time)

    # Create intermediate data reader used for processing sync
    reader = camera_bb2.right_frame.reader
    
    # Start the components
    camera_bb2.configure
    camera_bb2.start
    logger_bb2.start
    
    # Start processing
    log_replay.step
    
    while !log_replay.eof? do
		if reader.read_new then 
			log_replay.step
			print "#{log_replay.sample_index} over #{log_replay.size}\r"
		else
			sleep 0.01
		end
    end
    
    print 'The error in the end is normal'
end

