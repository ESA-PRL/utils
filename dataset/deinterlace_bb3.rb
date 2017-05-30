#! /usr/bin/env ruby

require 'orocos'
require 'orocos/log'
require 'rock/bundle'
require 'vizkit'

include Orocos

Bundles.initialize

# This ruby scripts takes the interlaced bb3 frame and saves three deinterlaced triplets in a new logfile

Orocos.run 'camera_bb3::Task' => 'camera_bb3' do
    
    # Declare logger of new ports
    logger_bb3 = Orocos.name_service.get 'camera_bb3_Logger'
    
    # New log destination
    logger_bb3.file = "bb3_deinterlaced.log"
    
    # New components to run on top of the log
    camera_bb3 = Orocos.name_service.get 'camera_bb3'
    Orocos.conf.apply(camera_bb3, ['default'], :override => true)
 
    # Open log file to be postprocessed
    if ARGV.size == 0 then
		log_replay = Orocos::Log::Replay.open("bb3.log")
    else
		log_replay = Orocos::Log::Replay.open(ARGV[0] + "bb3.log")
    end
    
    # Uses timestamp when data was acquired
    log_replay.use_sample_time = true
    
    # New connection (either to logfed ports or new components
    log_replay.camera_firewire_bb3.frame.connect_to(camera_bb3.frame_in)
        
    # Data to be logged
    logger_bb3.log(camera_bb3.left_frame)
    logger_bb3.log(camera_bb3.center_frame)
    logger_bb3.log(camera_bb3.right_frame)

    # Create intermediate data reader used for processing sync
    reader = camera_bb3.right_frame.reader
    
    # Start the components
    camera_bb3.configure
    camera_bb3.start
    logger_bb3.start    
    
    # start processing
    log_replay.step
    
    while !log_replay.eof? do
		if reader.read_new then 
			log_replay.step
			print "#{log_replay.sample_index} over #{log_replay.size}\r"
		else
			sleep 0.01
		end
    end

end

