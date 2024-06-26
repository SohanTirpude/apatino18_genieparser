expected_output = {
    "tcpproxy_statistics": {
        "total_connections": 32420,
        "max_concurrent_connections": 1466,
        "flow_entries_created": 32432,
        "flow_entries_deleted": 32432,
        "current_flow_entries": 0,
        "current_valid_flow_entries": 0,
        "current_connections": 0,
        "connections_in_progress": 0,
        "failed_connections": 12,
        "invalid_flow_entries": 0,
        "syncache_added": 32432,
        "syncache_not_added_nat_entry_null": 0,
        "syncache_not_added_mrkd_for_cleanup": 0,
        "syncache_not_added_flow_entry_null": 0,
        "syncache_not_added_flow_invalid": 0,
        "syncache_not_added_flow_is_in_use": 0,
        "syn_purge_enqueued": 0,
        "syn_purge_enqueue_failed": 0,
        "other_cleanup_enqueued": 0,
        "other_cleanup_enqueue_failed": 0,
        "stack_cleanup_enqueued": 11787,
        "stack_cleanup_enqueue_failed": 0,
        "timer_expire_cleanup_enqueued": 0,
        "timer_expire_cleanup_enqueue_failed": 0,
        "proxy_cleanup_enqueued": 20645,
        "proxy_cleanup_enqueue_failed": 0,
        "cleanup_req_watcher_called": 118623,
        "pre_tcp_flow_list_enq_failed": 0,
        "pre_tcp_flow_list_deq_failed_timer": 0,
        "pre_tcp_flow_list_deq_failed_accept": 0,
        "pre_tcp_flow_list_enq_success": 32432,
        "pre_tcp_flow_list_deq_cleanup": 0,
        "pre_tcp_flow_list_deq_accept": 32432,
        "pre_tcp_cleanup_timeout_update_count": 0,
        "total_flow_entries_pending_cleanup_0": 0,
        "total_cleanup_done": 32432,
        "num_stack_cb_with_null_ctx": 0,
        "vpath_cleanup_from_nmrx_thread": 0,
        "vpath_cleanup_from_ev_thread": 32432,
        "failed_conn_already_accepted_conn": 0,
        "ssl_init_failure": 0,
        "max_queue_length_work": 27,
        "current_queue_length_work": 0,
        "max_queue_length_ism": 0,
        "current_queue_length_ism": 0,
        "max_queue_length_sc": 0,
        "current_queue_length_sc": 0,
        "total_tx_enq_ign_due_to_conn_close": 15,
        "current_rx_epoll": 0,
        "current_tx_epoll": 0,
        "paused_by_tcp_tx_full": 0,
        "resumed_by_tcp_tx_below_threshold": 0,
        "paused_by_tcp_buffer_consumed": 0,
        "resumed_by_tcp_buffer_released": 0,
        "ssl_pause_done": 0,
        "ssl_resume_done": 0,
        "snort_pause_done": 0,
        "snort_resume_done": 0,
        "dre_pause_done": 0,
        "dre_resume_done": 0,
        "dre_resume_msg_to_be_sent": 0,
        "dre_resume_msg_sent": 0,
        "dre_bypass_received_from_peer": 0,
        "dre_bypass_hints_sent": 0,
        "dre_smb_bypass_success_received": 0,
        "dre_http_bypass_success_received": 0,
        "ev_ssl_pause_process": 0,
        "ev_snort_pause_process": 0,
        "ev_dre_pause_process": 0,
        "ev_ssl_snort_resume_process": 4728,
        "socket_pause_done": 0,
        "socket_resume_done": 4728,
        "ssl_pause_called": 0,
        "ssl_resume_called": 0,
        "async_events_sent": 31822,
        "async_events_processed": 31822,
        "tx_async_events_sent": 416778,
        "tx_async_events_recvd": 416777,
        "tx_async_events_processed": 416777,
        "failed_send": 0,
        "tcp_ssl_reset_initiated": 0,
        "tcp_snort_reset_initiated": 0,
        "tcp_dre_close_initiated": 0,
        "tcp_fin_received_from_clnt_svr": 44168,
        "tcp_reset_received_from_clnt_svr": 24995,
        "ssl_fin_received_sc": 0,
        "ssl_reset_received_sc": 0,
        "sc_fin_received_ssl": 0,
        "sc_reset_received_ssl": 0,
        "ssl_fin_received_tcp": 0,
        "ssl_reset_received_tcp": 0,
        "tcp_fin_processed": 44168,
        "tcp_fin_ignored_fd_already_closed": 0,
        "tcp_reset_processed": 20672,
        "svc_reset_processed": 0,
        "flow_cleaned_with_client_data": 0,
        "flow_cleaned_with_server_data": 0,
        "buffers_dropped_in_tx_socket_close": 1,
        "buffers_dropped_in_tx_not_writable": 0,
        "buffers_dropped_in_tx_socket_closed": 1,
        "tcp_4k_allocated_buffers": 416778,
        "tcp_16k_allocated_buffers": 0,
        "tcp_32k_allocated_buffers": 0,
        "tcp_128k_allocated_buffers": 0,
        "tcp_freed_buffers": 449210,
        "ssl_allocated_buffers": 0,
        "ssl_freed_buffers": 0,
        "tcp_received_buffers": 351938,
        "tcp_to_ssl_enqueued_buffers": 0,
        "ssl_to_svc_enqueued_buffers": 0,
        "svc_to_ssl_enqueued_buffers": 0,
        "ssl_to_tcp_enqueued_buffers": 0,
        "tcp_buffers_sent": 351933,
        "tcp_failed_buffers_allocations": 0,
        "tcp_failed_16k_buffers_allocations": 0,
        "tcp_failed_32k_buffers_allocations": 0,
        "tcp_failed_128k_buffers_allocations": 0,
        "ssl_failed_buffers_allocations": 0,
        "rx_sock_bytes_read_512": 49486,
        "rx_sock_bytes_read_1024": 3207,
        "rx_sock_bytes_read_2048": 18568,
        "rx_sock_bytes_read_4096": 280677,
        "ssl_server_init": 0,
        "flows_dropped_snort_gbl_health_yellow": 0,
        "flows_dropped_snort_inst_health_yellow": 0,
        "flows_dropped_wcapi_channel_health_yellow": 0,
        "total_wcapi_snd_flow_create_svc_chain_failed": 0,
        "total_wcapi_snd_flow_delete_svc_chain_failed": 0,
        "total_wcapi_send_data_svc_chain_failed": 0,
        "total_wcapi_send_close_svc_chain_failed": 0,
        "total_tx_enqueue_failed": 0,
        "total_cleanup_flow_msg_add_to_wk_q_failed": 0,
        "total_cleanup_flow_msg_added_to_wk_q": 0,
        "total_cleanup_flow_msg_rcvd_in_wk_q": 0,
        "total_cleanup_flow_ignored_already_done": 0,
        "total_cleanup_ssl_msg_add_to_wk_q_failed": 0,
        "total_ssl_trigger_reset_msg_to_wk_q_failed": 0,
        "total_uhi_mmap": 7793,
        "total_uhi_munmap": 0,
        "total_uhi_page_alloc": 0,
        "total_uhi_page_alloc_retry": 0,
        "total_uhi_page_alloc_failed": 0,
        "total_uhi_page_alloc_failed_invalid_size": 0,
        "total_uhi_page_free": 0,
        "total_enable_rx_enqueued": 0,
        "total_enable_rx_called": 0,
        "total_enable_rx_process_done": 0,
        "total_enable_rx_enqueue_failed": 0,
        "total_enable_rx_process_failed": 0,
        "total_enable_rx_socket_on_client_stack_close": 11228,
        "total_enable_rx_socket_on_server_stack_close": 20594,
        "unified_logging_msg_received": 0,
        "unified_logging_drop_data_too_long": 0,
        "unified_logging_enqueue_success": 0,
        "unified_logging_dequeue_success": 0,
        "unified_logging_deq_fail_not_enough_space": 0,
        "flow_stats_add_failure_count": 0,
        "flow_stats_delete_failure_count": 0,
        "aoim_sync_started": 0,
        "aoim_sync_completed": 0,
        "aoim_sync_errored": 0,
    }
}
