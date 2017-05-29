#! /usr/bin/env ruby

require 'pocolog'
include Pocolog

file = Logfiles.new File.open(ARGV[0] + "hdpr_unit_360.0.log")
data_stream = file.stream("/pancam_360.frame")
data_stream.samples.each do |time, asd|
    # Get the position difference between now and the last cycle for motor 0
    puts "frame"
    puts time
end
