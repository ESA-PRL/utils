tmux new-session -d -s 'PingList' -n pinglist 'ping 192.168.1.1'
tmux split-window -v 'ping 192.168.1.2'
tmux split-window -v 'ping 192.168.1.254'
tmux split-window -v 'ping 192.168.1.200'
tmux split-window -v 'ping 192.168.1.201'
tmux select-layout even-vertical
tmux split-window -v 'ping 192.168.1.202'
tmux select-layout even-vertical
tmux attach
