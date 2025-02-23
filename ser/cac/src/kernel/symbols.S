.section .symbols

.extern __assert_failed
.type __assert_failed, @function
.extern __kernel_arch
.type __kernel_arch, @function
.extern __kernel_build_date
.type __kernel_build_date, @function
.extern __kernel_build_time
.type __kernel_build_time, @function
.extern __kernel_compiler_version
.type __kernel_compiler_version, @function
.extern __kernel_name
.type __kernel_name, @function
.extern __kernel_version_codename
.type __kernel_version_codename, @function
.extern __kernel_version_format
.type __kernel_version_format, @function
.extern __kernel_version_lower
.type __kernel_version_lower, @function
.extern __kernel_version_major
.type __kernel_version_major, @function
.extern __kernel_version_minor
.type __kernel_version_minor, @function
.extern __kernel_version_suffix
.type __kernel_version_suffix, @function
.extern _ap_bootstrap_end
.type _ap_bootstrap_end, @function
.extern _ap_bootstrap_gdtp
.type _ap_bootstrap_gdtp, @function
.extern _ap_bootstrap_start
.type _ap_bootstrap_start, @function
.extern _ap_stack_base
.type _ap_stack_base, @function
.extern _irq0
.type _irq0, @function
.extern _irq1
.type _irq1, @function
.extern _irq10
.type _irq10, @function
.extern _irq11
.type _irq11, @function
.extern _irq12
.type _irq12, @function
.extern _irq13
.type _irq13, @function
.extern _irq14
.type _irq14, @function
.extern _irq15
.type _irq15, @function
.extern _irq2
.type _irq2, @function
.extern _irq3
.type _irq3, @function
.extern _irq4
.type _irq4, @function
.extern _irq5
.type _irq5, @function
.extern _irq6
.type _irq6, @function
.extern _irq7
.type _irq7, @function
.extern _irq8
.type _irq8, @function
.extern _irq9
.type _irq9, @function
.extern _isr0
.type _isr0, @function
.extern _isr1
.type _isr1, @function
.extern _isr10
.type _isr10, @function
.extern _isr11
.type _isr11, @function
.extern _isr12
.type _isr12, @function
.extern _isr123
.type _isr123, @function
.extern _isr124
.type _isr124, @function
.extern _isr125
.type _isr125, @function
.extern _isr126
.type _isr126, @function
.extern _isr127
.type _isr127, @function
.extern _isr13
.type _isr13, @function
.extern _isr14
.type _isr14, @function
.extern _isr15
.type _isr15, @function
.extern _isr16
.type _isr16, @function
.extern _isr17
.type _isr17, @function
.extern _isr18
.type _isr18, @function
.extern _isr19
.type _isr19, @function
.extern _isr2
.type _isr2, @function
.extern _isr20
.type _isr20, @function
.extern _isr21
.type _isr21, @function
.extern _isr22
.type _isr22, @function
.extern _isr23
.type _isr23, @function
.extern _isr24
.type _isr24, @function
.extern _isr25
.type _isr25, @function
.extern _isr26
.type _isr26, @function
.extern _isr27
.type _isr27, @function
.extern _isr28
.type _isr28, @function
.extern _isr29
.type _isr29, @function
.extern _isr3
.type _isr3, @function
.extern _isr30
.type _isr30, @function
.extern _isr31
.type _isr31, @function
.extern _isr4
.type _isr4, @function
.extern _isr5
.type _isr5, @function
.extern _isr6
.type _isr6, @function
.extern _isr7
.type _isr7, @function
.extern _isr8
.type _isr8, @function
.extern _isr9
.type _isr9, @function
.extern _modules_mutex
.type _modules_mutex, @function
.extern _modules_table
.type _modules_table, @function
.extern _ret_from_preempt_source
.type _ret_from_preempt_source, @function
.extern ap_main
.type ap_main, @function
.extern arch_boot_time
.type arch_boot_time, @function
.extern arch_clock_initialize
.type arch_clock_initialize, @function
.extern arch_cpu_mhz
.type arch_cpu_mhz, @function
.extern arch_dump_traceback
.type arch_dump_traceback, @function
.extern arch_enter_signal_handler
.type arch_enter_signal_handler, @function
.extern arch_enter_tasklet
.type arch_enter_tasklet, @function
.extern arch_enter_user
.type arch_enter_user, @function
.extern arch_fatal
.type arch_fatal, @function
.extern arch_fatal_prepare
.type arch_fatal_prepare, @function
.extern arch_framebuffer_initialize
.type arch_framebuffer_initialize, @function
.extern arch_get_cmdline
.type arch_get_cmdline, @function
.extern arch_get_loader
.type arch_get_loader, @function
.extern arch_pause
.type arch_pause, @function
.extern arch_perf_timer
.type arch_perf_timer, @function
.extern arch_reboot
.type arch_reboot, @function
.extern arch_restore_context
.type arch_restore_context, @function
.extern arch_restore_floating
.type arch_restore_floating, @function
.extern arch_resume_user
.type arch_resume_user, @function
.extern arch_return_from_signal_handler
.type arch_return_from_signal_handler, @function
.extern arch_save_context
.type arch_save_context, @function
.extern arch_save_floating
.type arch_save_floating, @function
.extern arch_set_core_base
.type arch_set_core_base, @function
.extern arch_set_kernel_stack
.type arch_set_kernel_stack, @function
.extern arch_set_tls_base
.type arch_set_tls_base, @function
.extern arch_stack_pointer
.type arch_stack_pointer, @function
.extern arch_syscall_arg0
.type arch_syscall_arg0, @function
.extern arch_syscall_arg1
.type arch_syscall_arg1, @function
.extern arch_syscall_arg2
.type arch_syscall_arg2, @function
.extern arch_syscall_arg3
.type arch_syscall_arg3, @function
.extern arch_syscall_arg4
.type arch_syscall_arg4, @function
.extern arch_syscall_number
.type arch_syscall_number, @function
.extern arch_syscall_return
.type arch_syscall_return, @function
.extern arch_tlb_shootdown
.type arch_tlb_shootdown, @function
.extern arch_update_clock
.type arch_update_clock, @function
.extern arch_user_ip
.type arch_user_ip, @function
.extern arch_wakeup_others
.type arch_wakeup_others, @function
.extern args_parse
.type args_parse, @function
.extern args_present
.type args_present, @function
.extern args_value
.type args_value, @function
.extern atoi
.type atoi, @function
.extern bss_start
.type bss_start, @function
.extern calculate_ipv4_checksum
.type calculate_ipv4_checksum, @function
.extern calculate_tcp_checksum
.type calculate_tcp_checksum, @function
.extern calloc
.type calloc, @function
.extern canonicalize_path
.type canonicalize_path, @function
.extern chmod_fs
.type chmod_fs, @function
.extern chown_fs
.type chown_fs, @function
.extern clone
.type clone, @function
.extern clone_fs
.type clone_fs, @function
.extern close_fs
.type close_fs, @function
.extern close_pipe
.type close_pipe, @function
.extern close_pty_master
.type close_pty_master, @function
.extern close_pty_slave
.type close_pty_slave, @function
.extern console_initialize
.type console_initialize, @function
.extern console_set_output
.type console_set_output, @function
.extern copy_page_maybe
.type copy_page_maybe, @function
.extern create_file_fs
.type create_file_fs, @function
.extern debug_print_vfs_tree
.type debug_print_vfs_tree, @function
.extern debug_print_vfs_tree_node
.type debug_print_vfs_tree_node, @function
.extern deflate_decompress
.type deflate_decompress, @function
.extern dprintf
.type dprintf, @function
.extern elf_exec
.type elf_exec, @function
.extern elf_module
.type elf_module, @function
.extern end
.type end, @function
.extern exec
.type exec, @function
.extern exec_shebang
.type exec_shebang, @function
.extern fbterm_draw_logo
.type fbterm_draw_logo, @function
.extern fbterm_initialize
.type fbterm_initialize, @function
.extern fbterm_reset
.type fbterm_reset, @function
.extern fbterm_write
.type fbterm_write, @function
.extern finddir_fs
.type finddir_fs, @function
.extern fixed_dists
.type fixed_dists, @function
.extern fixed_lengths
.type fixed_lengths, @function
.extern fmts
.type fmts, @function
.extern fork
.type fork, @function
.extern fprintf
.type fprintf, @function
.extern fpu_initialize
.type fpu_initialize, @function
.extern framebuffer_initialize
.type framebuffer_initialize, @function
.extern free
.type free, @function
.extern free_page_maybe
.type free_page_maybe, @function
.extern fs_root
.type fs_root, @function
.extern fs_tree
.type fs_tree, @function
.extern fs_types
.type fs_types, @function
.extern gdt
.type gdt, @function
.extern gdt_copy_to_trampoline
.type gdt_copy_to_trampoline, @function
.extern gdt_install
.type gdt_install, @function
.extern generic_main
.type generic_main, @function
.extern generic_startup
.type generic_startup, @function
.extern get_irq_handler
.type get_irq_handler, @function
.extern get_mount_point
.type get_mount_point, @function
.extern get_next_pid
.type get_next_pid, @function
.extern gettimeofday
.type gettimeofday, @function
.extern group_send_signal
.type group_send_signal, @function
.extern gzip_decompress
.type gzip_decompress, @function
.extern gzip_inputPtr
.type gzip_inputPtr, @function
.extern gzip_outputPtr
.type gzip_outputPtr, @function
.extern handle_signal
.type handle_signal, @function
.extern has_permission
.type has_permission, @function
.extern hashmap_create
.type hashmap_create, @function
.extern hashmap_create_int
.type hashmap_create_int, @function
.extern hashmap_free
.type hashmap_free, @function
.extern hashmap_get
.type hashmap_get, @function
.extern hashmap_has
.type hashmap_has, @function
.extern hashmap_int_comp
.type hashmap_int_comp, @function
.extern hashmap_int_dupe
.type hashmap_int_dupe, @function
.extern hashmap_int_hash
.type hashmap_int_hash, @function
.extern hashmap_is_empty
.type hashmap_is_empty, @function
.extern hashmap_keys
.type hashmap_keys, @function
.extern hashmap_remove
.type hashmap_remove, @function
.extern hashmap_set
.type hashmap_set, @function
.extern hashmap_string_comp
.type hashmap_string_comp, @function
.extern hashmap_string_dupe
.type hashmap_string_dupe, @function
.extern hashmap_string_hash
.type hashmap_string_hash, @function
.extern hashmap_values
.type hashmap_values, @function
.extern heap_base_pd
.type heap_base_pd, @function
.extern heap_base_pml
.type heap_base_pml, @function
.extern heap_base_pt
.type heap_base_pt, @function
.extern high_base_pml
.type high_base_pml, @function
.extern idt_ap_install
.type idt_ap_install, @function
.extern idt_install
.type idt_install, @function
.extern idt_set_gate
.type idt_set_gate, @function
.extern init_page_region
.type init_page_region, @function
.extern initialize_process_tree
.type initialize_process_tree, @function
.extern inportb
.type inportb, @function
.extern inportl
.type inportl, @function
.extern inports
.type inports, @function
.extern inportsm
.type inportsm, @function
.extern ioctl_fs
.type ioctl_fs, @function
.extern ioctl_pty_master
.type ioctl_pty_master, @function
.extern ioctl_pty_slave
.type ioctl_pty_slave, @function
.extern ipv4_install
.type ipv4_install, @function
.extern irq_ack
.type irq_ack, @function
.extern irq_install_handler
.type irq_install_handler, @function
.extern is_valid_process
.type is_valid_process, @function
.extern isr_common
.type isr_common, @function
.extern isr_handler
.type isr_handler, @function
.extern isr_handler_inner
.type isr_handler_inner, @function
.extern kernel_args_map
.type kernel_args_map, @function
.extern kmain
.type kmain, @function
.extern kopen
.type kopen, @function
.extern kopen_recur
.type kopen_recur, @function
.extern ksym_bind
.type ksym_bind, @function
.extern ksym_get_map
.type ksym_get_map, @function
.extern ksym_install
.type ksym_install, @function
.extern ksym_list
.type ksym_list, @function
.extern ksym_lookup
.type ksym_lookup, @function
.extern lapic_final
.type lapic_final, @function
.extern lapic_read
.type lapic_read, @function
.extern lapic_send_ipi
.type lapic_send_ipi, @function
.extern lapic_write
.type lapic_write, @function
.extern large_font
.type large_font, @function
.extern lfb_device
.type lfb_device, @function
.extern lfb_driver_name
.type lfb_driver_name, @function
.extern lfb_memsize
.type lfb_memsize, @function
.extern lfb_qemu_mmio
.type lfb_qemu_mmio, @function
.extern lfb_resolution_b
.type lfb_resolution_b, @function
.extern lfb_resolution_impl
.type lfb_resolution_impl, @function
.extern lfb_resolution_s
.type lfb_resolution_s, @function
.extern lfb_resolution_x
.type lfb_resolution_x, @function
.extern lfb_resolution_y
.type lfb_resolution_y, @function
.extern lfb_set_resolution
.type lfb_set_resolution, @function
.extern lfb_use_write_combining
.type lfb_use_write_combining, @function
.extern lfb_vid_memory
.type lfb_vid_memory, @function
.extern lfind
.type lfind, @function
.extern list_append
.type list_append, @function
.extern list_append_after
.type list_append_after, @function
.extern list_append_before
.type list_append_before, @function
.extern list_copy
.type list_copy, @function
.extern list_create
.type list_create, @function
.extern list_delete
.type list_delete, @function
.extern list_dequeue
.type list_dequeue, @function
.extern list_destroy
.type list_destroy, @function
.extern list_find
.type list_find, @function
.extern list_free
.type list_free, @function
.extern list_index
.type list_index, @function
.extern list_index_of
.type list_index_of, @function
.extern list_insert
.type list_insert, @function
.extern list_insert_after
.type list_insert_after, @function
.extern list_insert_before
.type list_insert_before, @function
.extern list_merge
.type list_merge, @function
.extern list_pop
.type list_pop, @function
.extern list_remove
.type list_remove, @function
.extern load_processor_info
.type load_processor_info, @function
.extern loopbook_install
.type loopbook_install, @function
.extern low_base_pmls
.type low_base_pmls, @function
.extern make_pipe
.type make_pipe, @function
.extern make_process_ready
.type make_process_ready, @function
.extern make_unix_pipe
.type make_unix_pipe, @function
.extern malloc
.type malloc, @function
.extern map_vfs_directory
.type map_vfs_directory, @function
.extern mboot2_find_next
.type mboot2_find_next, @function
.extern mboot2_find_tag
.type mboot2_find_tag, @function
.extern mboot_is_2
.type mboot_is_2, @function
.extern mboot_struct
.type mboot_struct, @function
.extern mboot_unmark_valid_memory
.type mboot_unmark_valid_memory, @function
.extern memchr
.type memchr, @function
.extern memcmp
.type memcmp, @function
.extern memcpy
.type memcpy, @function
.extern memmove
.type memmove, @function
.extern memrchr
.type memrchr, @function
.extern memset
.type memset, @function
.extern memsetw
.type memsetw, @function
.extern mkdir_fs
.type mkdir_fs, @function
.extern mmu_allocate_a_frame
.type mmu_allocate_a_frame, @function
.extern mmu_allocate_n_frames
.type mmu_allocate_n_frames, @function
.extern mmu_clone
.type mmu_clone, @function
.extern mmu_copy_on_write
.type mmu_copy_on_write, @function
.extern mmu_count_shm
.type mmu_count_shm, @function
.extern mmu_count_user
.type mmu_count_user, @function
.extern mmu_first_frame
.type mmu_first_frame, @function
.extern mmu_first_n_frames
.type mmu_first_n_frames, @function
.extern mmu_frame_allocate
.type mmu_frame_allocate, @function
.extern mmu_frame_clear
.type mmu_frame_clear, @function
.extern mmu_frame_map_address
.type mmu_frame_map_address, @function
.extern mmu_frame_release
.type mmu_frame_release, @function
.extern mmu_frame_set
.type mmu_frame_set, @function
.extern mmu_frame_test
.type mmu_frame_test, @function
.extern mmu_free
.type mmu_free, @function
.extern mmu_get_kernel_directory
.type mmu_get_kernel_directory, @function
.extern mmu_get_page
.type mmu_get_page, @function
.extern mmu_get_page_deep
.type mmu_get_page_deep, @function
.extern mmu_get_page_other
.type mmu_get_page_other, @function
.extern mmu_init
.type mmu_init, @function
.extern mmu_invalidate
.type mmu_invalidate, @function
.extern mmu_map_from_physical
.type mmu_map_from_physical, @function
.extern mmu_map_mmio_region
.type mmu_map_mmio_region, @function
.extern mmu_map_module
.type mmu_map_module, @function
.extern mmu_map_to_physical
.type mmu_map_to_physical, @function
.extern mmu_set_directory
.type mmu_set_directory, @function
.extern mmu_total_memory
.type mmu_total_memory, @function
.extern mmu_unmap_module
.type mmu_unmap_module, @function
.extern mmu_unmap_user
.type mmu_unmap_user, @function
.extern mmu_used_memory
.type mmu_used_memory, @function
.extern mmu_validate_user_pointer
.type mmu_validate_user_pointer, @function
.extern modules_get_list
.type modules_get_list, @function
.extern modules_install
.type modules_install, @function
.extern mount_multiboot_ramdisks
.type mount_multiboot_ramdisks, @function
.extern mutex_acquire
.type mutex_acquire, @function
.extern mutex_init
.type mutex_init, @function
.extern mutex_release
.type mutex_release, @function
.extern net_accept
.type net_accept, @function
.extern net_add_interface
.type net_add_interface, @function
.extern net_arp_ask
.type net_arp_ask, @function
.extern net_arp_cache
.type net_arp_cache, @function
.extern net_arp_cache_add
.type net_arp_cache_add, @function
.extern net_arp_cache_get
.type net_arp_cache_get, @function
.extern net_arp_cache_lock
.type net_arp_cache_lock, @function
.extern net_arp_handle
.type net_arp_handle, @function
.extern net_bind
.type net_bind, @function
.extern net_connect
.type net_connect, @function
.extern net_eth_handle
.type net_eth_handle, @function
.extern net_eth_send
.type net_eth_send, @function
.extern net_getpeername
.type net_getpeername, @function
.extern net_getsockname
.type net_getsockname, @function
.extern net_getsockopt
.type net_getsockopt, @function
.extern net_if_any
.type net_if_any, @function
.extern net_if_lookup
.type net_if_lookup, @function
.extern net_if_route
.type net_if_route, @function
.extern net_install
.type net_install, @function
.extern net_ipv4_handle
.type net_ipv4_handle, @function
.extern net_ipv4_send
.type net_ipv4_send, @function
.extern net_ipv4_socket
.type net_ipv4_socket, @function
.extern net_listen
.type net_listen, @function
.extern net_raw_socket
.type net_raw_socket, @function
.extern net_raw_sockets_list
.type net_raw_sockets_list, @function
.extern net_raw_sockets_lock
.type net_raw_sockets_lock, @function
.extern net_recv
.type net_recv, @function
.extern net_send
.type net_send, @function
.extern net_setsockopt
.type net_setsockopt, @function
.extern net_shutdown
.type net_shutdown, @function
.extern net_so_socket
.type net_so_socket, @function
.extern net_sock_add
.type net_sock_add, @function
.extern net_sock_alert
.type net_sock_alert, @function
.extern net_sock_create
.type net_sock_create, @function
.extern net_sock_get
.type net_sock_get, @function
.extern net_socket
.type net_socket, @function
.extern next_ready_process
.type next_ready_process, @function
.extern now
.type now, @function
.extern open_fs
.type open_fs, @function
.extern open_pipe
.type open_pipe, @function
.extern open_pty_master
.type open_pty_master, @function
.extern open_pty_slave
.type open_pty_slave, @function
.extern outportb
.type outportb, @function
.extern outportl
.type outportl, @function
.extern outports
.type outports, @function
.extern outportsm
.type outportsm, @function
.extern packetfs_initialize
.type packetfs_initialize, @function
.extern pat_initialize
.type pat_initialize, @function
.extern pci_find_type
.type pci_find_type, @function
.extern pci_get_interrupt
.type pci_get_interrupt, @function
.extern pci_read_field
.type pci_read_field, @function
.extern pci_scan
.type pci_scan, @function
.extern pci_scan_bus
.type pci_scan_bus, @function
.extern pci_scan_func
.type pci_scan_func, @function
.extern pci_scan_slot
.type pci_scan_slot, @function
.extern pci_write_field
.type pci_write_field, @function
.extern pcie_ecam_phys
.type pcie_ecam_phys, @function
.extern phys
.type phys, @function
.extern pic_initialize
.type pic_initialize, @function
.extern pipe_destroy
.type pipe_destroy, @function
.extern pipe_size
.type pipe_size, @function
.extern pipe_unsize
.type pipe_unsize, @function
.extern pit_initialize
.type pit_initialize, @function
.extern pit_interrupt
.type pit_interrupt, @function
.extern portio_initialize
.type portio_initialize, @function
.extern printf
.type printf, @function
.extern printf_output
.type printf_output, @function
.extern process_alert_node
.type process_alert_node, @function
.extern process_alert_node_locked
.type process_alert_node_locked, @function
.extern process_append_fd
.type process_append_fd, @function
.extern process_awaken_from_fswait
.type process_awaken_from_fswait, @function
.extern process_awaken_signal
.type process_awaken_signal, @function
.extern process_check_signals
.type process_check_signals, @function
.extern process_compare
.type process_compare, @function
.extern process_delete
.type process_delete, @function
.extern process_from_pid
.type process_from_pid, @function
.extern process_get_parent
.type process_get_parent, @function
.extern process_is_ready
.type process_is_ready, @function
.extern process_list
.type process_list, @function
.extern process_move_fd
.type process_move_fd, @function
.extern process_queue
.type process_queue, @function
.extern process_reap
.type process_reap, @function
.extern process_reap_later
.type process_reap_later, @function
.extern process_release_directory
.type process_release_directory, @function
.extern process_timeout_sleep
.type process_timeout_sleep, @function
.extern process_tree
.type process_tree, @function
.extern process_wait_nodes
.type process_wait_nodes, @function
.extern processor_count
.type processor_count, @function
.extern processor_local_data
.type processor_local_data, @function
.extern procfs_initialize
.type procfs_initialize, @function
.extern procfs_install
.type procfs_install, @function
.extern procfs_printf
.type procfs_printf, @function
.extern ps2_mouse_alternate
.type ps2_mouse_alternate, @function
.extern ps2hid_install
.type ps2hid_install, @function
.extern ptr_validate
.type ptr_validate, @function
.extern ptrace_attach
.type ptrace_attach, @function
.extern ptrace_continue
.type ptrace_continue, @function
.extern ptrace_detach
.type ptrace_detach, @function
.extern ptrace_getregs
.type ptrace_getregs, @function
.extern ptrace_handle
.type ptrace_handle, @function
.extern ptrace_peek
.type ptrace_peek, @function
.extern ptrace_poke
.type ptrace_poke, @function
.extern ptrace_self
.type ptrace_self, @function
.extern ptrace_signal
.type ptrace_signal, @function
.extern ptrace_signals_only
.type ptrace_signals_only, @function
.extern ptrace_singlestep
.type ptrace_singlestep, @function
.extern pty_available_input
.type pty_available_input, @function
.extern pty_available_output
.type pty_available_output, @function
.extern pty_create
.type pty_create, @function
.extern pty_install
.type pty_install, @function
.extern pty_ioctl
.type pty_ioctl, @function
.extern pty_master_create
.type pty_master_create, @function
.extern pty_new
.type pty_new, @function
.extern pty_slave_create
.type pty_slave_create, @function
.extern ramdisk_mount
.type ramdisk_mount, @function
.extern rand
.type rand, @function
.extern random_initialize
.type random_initialize, @function
.extern read_cmos
.type read_cmos, @function
.extern read_fs
.type read_fs, @function
.extern read_pipe
.type read_pipe, @function
.extern read_pty_master
.type read_pty_master, @function
.extern read_pty_slave
.type read_pty_slave, @function
.extern readdir_fs
.type readdir_fs, @function
.extern readlink_fs
.type readlink_fs, @function
.extern realloc
.type realloc, @function
.extern reap_queue
.type reap_queue, @function
.extern refcount_dec
.type refcount_dec, @function
.extern refcount_inc
.type refcount_inc, @function
.extern relative_time
.type relative_time, @function
.extern return_from_signal_handler
.type return_from_signal_handler, @function
.extern rfind
.type rfind, @function
.extern ring_buffer_alert_waiters
.type ring_buffer_alert_waiters, @function
.extern ring_buffer_available
.type ring_buffer_available, @function
.extern ring_buffer_create
.type ring_buffer_create, @function
.extern ring_buffer_destroy
.type ring_buffer_destroy, @function
.extern ring_buffer_eof
.type ring_buffer_eof, @function
.extern ring_buffer_interrupt
.type ring_buffer_interrupt, @function
.extern ring_buffer_read
.type ring_buffer_read, @function
.extern ring_buffer_select_wait
.type ring_buffer_select_wait, @function
.extern ring_buffer_size
.type ring_buffer_size, @function
.extern ring_buffer_unread
.type ring_buffer_unread, @function
.extern ring_buffer_write
.type ring_buffer_write, @function
.extern sbrk
.type sbrk, @function
.extern selectcheck_fs
.type selectcheck_fs, @function
.extern selectwait_fs
.type selectwait_fs, @function
.extern send_signal
.type send_signal, @function
.extern serial_handler_ac
.type serial_handler_ac, @function
.extern serial_handler_bd
.type serial_handler_bd, @function
.extern serial_initialize
.type serial_initialize, @function
.extern settimeofday
.type settimeofday, @function
.extern shm_install
.type shm_install, @function
.extern shm_obtain
.type shm_obtain, @function
.extern shm_release
.type shm_release, @function
.extern shm_release_all
.type shm_release_all, @function
.extern shm_tree
.type shm_tree, @function
.extern signal_await
.type signal_await, @function
.extern sleep_on
.type sleep_on, @function
.extern sleep_on_unlocking
.type sleep_on_unlocking, @function
.extern sleep_queue
.type sleep_queue, @function
.extern sleep_until
.type sleep_until, @function
.extern smp_initialize
.type smp_initialize, @function
.extern snd_install
.type snd_install, @function
.extern snd_register
.type snd_register, @function
.extern snd_request_buf
.type snd_request_buf, @function
.extern snd_unregister
.type snd_unregister, @function
.extern snprintf
.type snprintf, @function
.extern sock_generic_check
.type sock_generic_check, @function
.extern sock_generic_close
.type sock_generic_close, @function
.extern sock_generic_ioctl
.type sock_generic_ioctl, @function
.extern sock_generic_wait
.type sock_generic_wait, @function
.extern sock_tcp_getpeername
.type sock_tcp_getpeername, @function
.extern sock_tcp_getsockname
.type sock_tcp_getsockname, @function
.extern sock_tcp_read
.type sock_tcp_read, @function
.extern sock_tcp_write
.type sock_tcp_write, @function
.extern spawn_init
.type spawn_init, @function
.extern spawn_kidle
.type spawn_kidle, @function
.extern spawn_process
.type spawn_process, @function
.extern spawn_worker_thread
.type spawn_worker_thread, @function
.extern stack_top
.type stack_top, @function
.extern start
.type start, @function
.extern startswith
.type startswith, @function
.extern stpcpy
.type stpcpy, @function
.extern strchr
.type strchr, @function
.extern strchrnul
.type strchrnul, @function
.extern strcmp
.type strcmp, @function
.extern strcpy
.type strcpy, @function
.extern strcspn
.type strcspn, @function
.extern strdup
.type strdup, @function
.extern strlen
.type strlen, @function
.extern strpbrk
.type strpbrk, @function
.extern strrchr
.type strrchr, @function
.extern strspn
.type strspn, @function
.extern strstr
.type strstr, @function
.extern strtok_r
.type strtok_r, @function
.extern switch_next
.type switch_next, @function
.extern switch_task
.type switch_task, @function
.extern symlink_fs
.type symlink_fs, @function
.extern sys_access
.type sys_access, @function
.extern sys_chdir
.type sys_chdir, @function
.extern sys_chmod
.type sys_chmod, @function
.extern sys_chown
.type sys_chown, @function
.extern sys_clone
.type sys_clone, @function
.extern sys_close
.type sys_close, @function
.extern sys_dup2
.type sys_dup2, @function
.extern sys_execve
.type sys_execve, @function
.extern sys_exit
.type sys_exit, @function
.extern sys_fork
.type sys_fork, @function
.extern sys_fswait
.type sys_fswait, @function
.extern sys_fswait_multi
.type sys_fswait_multi, @function
.extern sys_fswait_timeout
.type sys_fswait_timeout, @function
.extern sys_getcwd
.type sys_getcwd, @function
.extern sys_getegid
.type sys_getegid, @function
.extern sys_geteuid
.type sys_geteuid, @function
.extern sys_getgid
.type sys_getgid, @function
.extern sys_getgroups
.type sys_getgroups, @function
.extern sys_gethostname
.type sys_gethostname, @function
.extern sys_getpgid
.type sys_getpgid, @function
.extern sys_getpid
.type sys_getpid, @function
.extern sys_gettid
.type sys_gettid, @function
.extern sys_gettimeofday
.type sys_gettimeofday, @function
.extern sys_getuid
.type sys_getuid, @function
.extern sys_ioctl
.type sys_ioctl, @function
.extern sys_kill
.type sys_kill, @function
.extern sys_lstat
.type sys_lstat, @function
.extern sys_mkdir
.type sys_mkdir, @function
.extern sys_mount
.type sys_mount, @function
.extern sys_open
.type sys_open, @function
.extern sys_openpty
.type sys_openpty, @function
.extern sys_pipe
.type sys_pipe, @function
.extern sys_read
.type sys_read, @function
.extern sys_readdir
.type sys_readdir, @function
.extern sys_readlink
.type sys_readlink, @function
.extern sys_reboot
.type sys_reboot, @function
.extern sys_sbrk
.type sys_sbrk, @function
.extern sys_seek
.type sys_seek, @function
.extern sys_setgid
.type sys_setgid, @function
.extern sys_setgroups
.type sys_setgroups, @function
.extern sys_sethostname
.type sys_sethostname, @function
.extern sys_setpgid
.type sys_setpgid, @function
.extern sys_setsid
.type sys_setsid, @function
.extern sys_settimeofday
.type sys_settimeofday, @function
.extern sys_setuid
.type sys_setuid, @function
.extern sys_shm_obtain
.type sys_shm_obtain, @function
.extern sys_shm_release
.type sys_shm_release, @function
.extern sys_sigaction
.type sys_sigaction, @function
.extern sys_signal
.type sys_signal, @function
.extern sys_sigpending
.type sys_sigpending, @function
.extern sys_sigprocmask
.type sys_sigprocmask, @function
.extern sys_sigsuspend_cur
.type sys_sigsuspend_cur, @function
.extern sys_sigwait
.type sys_sigwait, @function
.extern sys_sleep
.type sys_sleep, @function
.extern sys_sleepabs
.type sys_sleepabs, @function
.extern sys_stat
.type sys_stat, @function
.extern sys_statf
.type sys_statf, @function
.extern sys_symlink
.type sys_symlink, @function
.extern sys_sysfunc
.type sys_sysfunc, @function
.extern sys_times
.type sys_times, @function
.extern sys_umask
.type sys_umask, @function
.extern sys_uname
.type sys_uname, @function
.extern sys_unlink
.type sys_unlink, @function
.extern sys_waitpid
.type sys_waitpid, @function
.extern sys_write
.type sys_write, @function
.extern sys_yield
.type sys_yield, @function
.extern syscall_handler
.type syscall_handler, @function
.extern system
.type system, @function
.extern tarfs_register_init
.type tarfs_register_init, @function
.extern task_exit
.type task_exit, @function
.extern tasking_start
.type tasking_start, @function
.extern tmpfs_create
.type tmpfs_create, @function
.extern tmpfs_mount
.type tmpfs_mount, @function
.extern tmpfs_register_init
.type tmpfs_register_init, @function
.extern tokenize
.type tokenize, @function
.extern tree_break_off
.type tree_break_off, @function
.extern tree_count_children
.type tree_count_children, @function
.extern tree_create
.type tree_create, @function
.extern tree_destroy
.type tree_destroy, @function
.extern tree_find
.type tree_find, @function
.extern tree_find_parent
.type tree_find_parent, @function
.extern tree_free
.type tree_free, @function
.extern tree_node_create
.type tree_node_create, @function
.extern tree_node_destroy
.type tree_node_destroy, @function
.extern tree_node_find
.type tree_node_find, @function
.extern tree_node_find_parent
.type tree_node_find_parent, @function
.extern tree_node_free
.type tree_node_free, @function
.extern tree_node_insert_child
.type tree_node_insert_child, @function
.extern tree_node_insert_child_node
.type tree_node_insert_child_node, @function
.extern tree_node_parent_remove
.type tree_node_parent_remove, @function
.extern tree_node_remove
.type tree_node_remove, @function
.extern tree_remove
.type tree_remove, @function
.extern tree_remove_reparent_root
.type tree_remove_reparent_root, @function
.extern tree_set_root
.type tree_set_root, @function
.extern truncate_fs
.type truncate_fs, @function
.extern tsc_basis_time
.type tsc_basis_time, @function
.extern tsc_mhz
.type tsc_mhz, @function
.extern tty_input_process
.type tty_input_process, @function
.extern tty_output_process
.type tty_output_process, @function
.extern tty_output_process_slave
.type tty_output_process_slave, @function
.extern twom_high_pds
.type twom_high_pds, @function
.extern unlink_fs
.type unlink_fs, @function
.extern update_process_times
.type update_process_times, @function
.extern update_process_usage
.type update_process_usage, @function
.extern valloc
.type valloc, @function
.extern vfs_install
.type vfs_install, @function
.extern vfs_lock
.type vfs_lock, @function
.extern vfs_mount
.type vfs_mount, @function
.extern vfs_mount_type
.type vfs_mount_type, @function
.extern vfs_register
.type vfs_register, @function
.extern vsnprintf
.type vsnprintf, @function
.extern waitpid
.type waitpid, @function
.extern wakeup_queue
.type wakeup_queue, @function
.extern wakeup_queue_interrupted
.type wakeup_queue_interrupted, @function
.extern wakeup_queue_one
.type wakeup_queue_one, @function
.extern wakeup_sleepers
.type wakeup_sleepers, @function
.extern write_fs
.type write_fs, @function
.extern write_pipe
.type write_pipe, @function
.extern write_pty_master
.type write_pty_master, @function
.extern write_pty_slave
.type write_pty_slave, @function
.extern xtoi
.type xtoi, @function
.extern xvasprintf
.type xvasprintf, @function
.extern zero_initialize
.type zero_initialize, @function
.global kernel_symbols_start
kernel_symbols_start:

.quad __assert_failed
.asciz "__assert_failed"
.quad __kernel_arch
.asciz "__kernel_arch"
.quad __kernel_build_date
.asciz "__kernel_build_date"
.quad __kernel_build_time
.asciz "__kernel_build_time"
.quad __kernel_compiler_version
.asciz "__kernel_compiler_version"
.quad __kernel_name
.asciz "__kernel_name"
.quad __kernel_version_codename
.asciz "__kernel_version_codename"
.quad __kernel_version_format
.asciz "__kernel_version_format"
.quad __kernel_version_lower
.asciz "__kernel_version_lower"
.quad __kernel_version_major
.asciz "__kernel_version_major"
.quad __kernel_version_minor
.asciz "__kernel_version_minor"
.quad __kernel_version_suffix
.asciz "__kernel_version_suffix"
.quad _ap_bootstrap_end
.asciz "_ap_bootstrap_end"
.quad _ap_bootstrap_gdtp
.asciz "_ap_bootstrap_gdtp"
.quad _ap_bootstrap_start
.asciz "_ap_bootstrap_start"
.quad _ap_stack_base
.asciz "_ap_stack_base"
.quad _irq0
.asciz "_irq0"
.quad _irq1
.asciz "_irq1"
.quad _irq10
.asciz "_irq10"
.quad _irq11
.asciz "_irq11"
.quad _irq12
.asciz "_irq12"
.quad _irq13
.asciz "_irq13"
.quad _irq14
.asciz "_irq14"
.quad _irq15
.asciz "_irq15"
.quad _irq2
.asciz "_irq2"
.quad _irq3
.asciz "_irq3"
.quad _irq4
.asciz "_irq4"
.quad _irq5
.asciz "_irq5"
.quad _irq6
.asciz "_irq6"
.quad _irq7
.asciz "_irq7"
.quad _irq8
.asciz "_irq8"
.quad _irq9
.asciz "_irq9"
.quad _isr0
.asciz "_isr0"
.quad _isr1
.asciz "_isr1"
.quad _isr10
.asciz "_isr10"
.quad _isr11
.asciz "_isr11"
.quad _isr12
.asciz "_isr12"
.quad _isr123
.asciz "_isr123"
.quad _isr124
.asciz "_isr124"
.quad _isr125
.asciz "_isr125"
.quad _isr126
.asciz "_isr126"
.quad _isr127
.asciz "_isr127"
.quad _isr13
.asciz "_isr13"
.quad _isr14
.asciz "_isr14"
.quad _isr15
.asciz "_isr15"
.quad _isr16
.asciz "_isr16"
.quad _isr17
.asciz "_isr17"
.quad _isr18
.asciz "_isr18"
.quad _isr19
.asciz "_isr19"
.quad _isr2
.asciz "_isr2"
.quad _isr20
.asciz "_isr20"
.quad _isr21
.asciz "_isr21"
.quad _isr22
.asciz "_isr22"
.quad _isr23
.asciz "_isr23"
.quad _isr24
.asciz "_isr24"
.quad _isr25
.asciz "_isr25"
.quad _isr26
.asciz "_isr26"
.quad _isr27
.asciz "_isr27"
.quad _isr28
.asciz "_isr28"
.quad _isr29
.asciz "_isr29"
.quad _isr3
.asciz "_isr3"
.quad _isr30
.asciz "_isr30"
.quad _isr31
.asciz "_isr31"
.quad _isr4
.asciz "_isr4"
.quad _isr5
.asciz "_isr5"
.quad _isr6
.asciz "_isr6"
.quad _isr7
.asciz "_isr7"
.quad _isr8
.asciz "_isr8"
.quad _isr9
.asciz "_isr9"
.quad _modules_mutex
.asciz "_modules_mutex"
.quad _modules_table
.asciz "_modules_table"
.quad _ret_from_preempt_source
.asciz "_ret_from_preempt_source"
.quad ap_main
.asciz "ap_main"
.quad arch_boot_time
.asciz "arch_boot_time"
.quad arch_clock_initialize
.asciz "arch_clock_initialize"
.quad arch_cpu_mhz
.asciz "arch_cpu_mhz"
.quad arch_dump_traceback
.asciz "arch_dump_traceback"
.quad arch_enter_signal_handler
.asciz "arch_enter_signal_handler"
.quad arch_enter_tasklet
.asciz "arch_enter_tasklet"
.quad arch_enter_user
.asciz "arch_enter_user"
.quad arch_fatal
.asciz "arch_fatal"
.quad arch_fatal_prepare
.asciz "arch_fatal_prepare"
.quad arch_framebuffer_initialize
.asciz "arch_framebuffer_initialize"
.quad arch_get_cmdline
.asciz "arch_get_cmdline"
.quad arch_get_loader
.asciz "arch_get_loader"
.quad arch_pause
.asciz "arch_pause"
.quad arch_perf_timer
.asciz "arch_perf_timer"
.quad arch_reboot
.asciz "arch_reboot"
.quad arch_restore_context
.asciz "arch_restore_context"
.quad arch_restore_floating
.asciz "arch_restore_floating"
.quad arch_resume_user
.asciz "arch_resume_user"
.quad arch_return_from_signal_handler
.asciz "arch_return_from_signal_handler"
.quad arch_save_context
.asciz "arch_save_context"
.quad arch_save_floating
.asciz "arch_save_floating"
.quad arch_set_core_base
.asciz "arch_set_core_base"
.quad arch_set_kernel_stack
.asciz "arch_set_kernel_stack"
.quad arch_set_tls_base
.asciz "arch_set_tls_base"
.quad arch_stack_pointer
.asciz "arch_stack_pointer"
.quad arch_syscall_arg0
.asciz "arch_syscall_arg0"
.quad arch_syscall_arg1
.asciz "arch_syscall_arg1"
.quad arch_syscall_arg2
.asciz "arch_syscall_arg2"
.quad arch_syscall_arg3
.asciz "arch_syscall_arg3"
.quad arch_syscall_arg4
.asciz "arch_syscall_arg4"
.quad arch_syscall_number
.asciz "arch_syscall_number"
.quad arch_syscall_return
.asciz "arch_syscall_return"
.quad arch_tlb_shootdown
.asciz "arch_tlb_shootdown"
.quad arch_update_clock
.asciz "arch_update_clock"
.quad arch_user_ip
.asciz "arch_user_ip"
.quad arch_wakeup_others
.asciz "arch_wakeup_others"
.quad args_parse
.asciz "args_parse"
.quad args_present
.asciz "args_present"
.quad args_value
.asciz "args_value"
.quad atoi
.asciz "atoi"
.quad bss_start
.asciz "bss_start"
.quad calculate_ipv4_checksum
.asciz "calculate_ipv4_checksum"
.quad calculate_tcp_checksum
.asciz "calculate_tcp_checksum"
.quad calloc
.asciz "calloc"
.quad canonicalize_path
.asciz "canonicalize_path"
.quad chmod_fs
.asciz "chmod_fs"
.quad chown_fs
.asciz "chown_fs"
.quad clone
.asciz "clone"
.quad clone_fs
.asciz "clone_fs"
.quad close_fs
.asciz "close_fs"
.quad close_pipe
.asciz "close_pipe"
.quad close_pty_master
.asciz "close_pty_master"
.quad close_pty_slave
.asciz "close_pty_slave"
.quad console_initialize
.asciz "console_initialize"
.quad console_set_output
.asciz "console_set_output"
.quad copy_page_maybe
.asciz "copy_page_maybe"
.quad create_file_fs
.asciz "create_file_fs"
.quad debug_print_vfs_tree
.asciz "debug_print_vfs_tree"
.quad debug_print_vfs_tree_node
.asciz "debug_print_vfs_tree_node"
.quad deflate_decompress
.asciz "deflate_decompress"
.quad dprintf
.asciz "dprintf"
.quad elf_exec
.asciz "elf_exec"
.quad elf_module
.asciz "elf_module"
.quad end
.asciz "end"
.quad exec
.asciz "exec"
.quad exec_shebang
.asciz "exec_shebang"
.quad fbterm_draw_logo
.asciz "fbterm_draw_logo"
.quad fbterm_initialize
.asciz "fbterm_initialize"
.quad fbterm_reset
.asciz "fbterm_reset"
.quad fbterm_write
.asciz "fbterm_write"
.quad finddir_fs
.asciz "finddir_fs"
.quad fixed_dists
.asciz "fixed_dists"
.quad fixed_lengths
.asciz "fixed_lengths"
.quad fmts
.asciz "fmts"
.quad fork
.asciz "fork"
.quad fprintf
.asciz "fprintf"
.quad fpu_initialize
.asciz "fpu_initialize"
.quad framebuffer_initialize
.asciz "framebuffer_initialize"
.quad free
.asciz "free"
.quad free_page_maybe
.asciz "free_page_maybe"
.quad fs_root
.asciz "fs_root"
.quad fs_tree
.asciz "fs_tree"
.quad fs_types
.asciz "fs_types"
.quad gdt
.asciz "gdt"
.quad gdt_copy_to_trampoline
.asciz "gdt_copy_to_trampoline"
.quad gdt_install
.asciz "gdt_install"
.quad generic_main
.asciz "generic_main"
.quad generic_startup
.asciz "generic_startup"
.quad get_irq_handler
.asciz "get_irq_handler"
.quad get_mount_point
.asciz "get_mount_point"
.quad get_next_pid
.asciz "get_next_pid"
.quad gettimeofday
.asciz "gettimeofday"
.quad group_send_signal
.asciz "group_send_signal"
.quad gzip_decompress
.asciz "gzip_decompress"
.quad gzip_inputPtr
.asciz "gzip_inputPtr"
.quad gzip_outputPtr
.asciz "gzip_outputPtr"
.quad handle_signal
.asciz "handle_signal"
.quad has_permission
.asciz "has_permission"
.quad hashmap_create
.asciz "hashmap_create"
.quad hashmap_create_int
.asciz "hashmap_create_int"
.quad hashmap_free
.asciz "hashmap_free"
.quad hashmap_get
.asciz "hashmap_get"
.quad hashmap_has
.asciz "hashmap_has"
.quad hashmap_int_comp
.asciz "hashmap_int_comp"
.quad hashmap_int_dupe
.asciz "hashmap_int_dupe"
.quad hashmap_int_hash
.asciz "hashmap_int_hash"
.quad hashmap_is_empty
.asciz "hashmap_is_empty"
.quad hashmap_keys
.asciz "hashmap_keys"
.quad hashmap_remove
.asciz "hashmap_remove"
.quad hashmap_set
.asciz "hashmap_set"
.quad hashmap_string_comp
.asciz "hashmap_string_comp"
.quad hashmap_string_dupe
.asciz "hashmap_string_dupe"
.quad hashmap_string_hash
.asciz "hashmap_string_hash"
.quad hashmap_values
.asciz "hashmap_values"
.quad heap_base_pd
.asciz "heap_base_pd"
.quad heap_base_pml
.asciz "heap_base_pml"
.quad heap_base_pt
.asciz "heap_base_pt"
.quad high_base_pml
.asciz "high_base_pml"
.quad idt_ap_install
.asciz "idt_ap_install"
.quad idt_install
.asciz "idt_install"
.quad idt_set_gate
.asciz "idt_set_gate"
.quad init_page_region
.asciz "init_page_region"
.quad initialize_process_tree
.asciz "initialize_process_tree"
.quad inportb
.asciz "inportb"
.quad inportl
.asciz "inportl"
.quad inports
.asciz "inports"
.quad inportsm
.asciz "inportsm"
.quad ioctl_fs
.asciz "ioctl_fs"
.quad ioctl_pty_master
.asciz "ioctl_pty_master"
.quad ioctl_pty_slave
.asciz "ioctl_pty_slave"
.quad ipv4_install
.asciz "ipv4_install"
.quad irq_ack
.asciz "irq_ack"
.quad irq_install_handler
.asciz "irq_install_handler"
.quad is_valid_process
.asciz "is_valid_process"
.quad isr_common
.asciz "isr_common"
.quad isr_handler
.asciz "isr_handler"
.quad isr_handler_inner
.asciz "isr_handler_inner"
.quad kernel_args_map
.asciz "kernel_args_map"
.quad kmain
.asciz "kmain"
.quad kopen
.asciz "kopen"
.quad kopen_recur
.asciz "kopen_recur"
.quad ksym_bind
.asciz "ksym_bind"
.quad ksym_get_map
.asciz "ksym_get_map"
.quad ksym_install
.asciz "ksym_install"
.quad ksym_list
.asciz "ksym_list"
.quad ksym_lookup
.asciz "ksym_lookup"
.quad lapic_final
.asciz "lapic_final"
.quad lapic_read
.asciz "lapic_read"
.quad lapic_send_ipi
.asciz "lapic_send_ipi"
.quad lapic_write
.asciz "lapic_write"
.quad large_font
.asciz "large_font"
.quad lfb_device
.asciz "lfb_device"
.quad lfb_driver_name
.asciz "lfb_driver_name"
.quad lfb_memsize
.asciz "lfb_memsize"
.quad lfb_qemu_mmio
.asciz "lfb_qemu_mmio"
.quad lfb_resolution_b
.asciz "lfb_resolution_b"
.quad lfb_resolution_impl
.asciz "lfb_resolution_impl"
.quad lfb_resolution_s
.asciz "lfb_resolution_s"
.quad lfb_resolution_x
.asciz "lfb_resolution_x"
.quad lfb_resolution_y
.asciz "lfb_resolution_y"
.quad lfb_set_resolution
.asciz "lfb_set_resolution"
.quad lfb_use_write_combining
.asciz "lfb_use_write_combining"
.quad lfb_vid_memory
.asciz "lfb_vid_memory"
.quad lfind
.asciz "lfind"
.quad list_append
.asciz "list_append"
.quad list_append_after
.asciz "list_append_after"
.quad list_append_before
.asciz "list_append_before"
.quad list_copy
.asciz "list_copy"
.quad list_create
.asciz "list_create"
.quad list_delete
.asciz "list_delete"
.quad list_dequeue
.asciz "list_dequeue"
.quad list_destroy
.asciz "list_destroy"
.quad list_find
.asciz "list_find"
.quad list_free
.asciz "list_free"
.quad list_index
.asciz "list_index"
.quad list_index_of
.asciz "list_index_of"
.quad list_insert
.asciz "list_insert"
.quad list_insert_after
.asciz "list_insert_after"
.quad list_insert_before
.asciz "list_insert_before"
.quad list_merge
.asciz "list_merge"
.quad list_pop
.asciz "list_pop"
.quad list_remove
.asciz "list_remove"
.quad load_processor_info
.asciz "load_processor_info"
.quad loopbook_install
.asciz "loopbook_install"
.quad low_base_pmls
.asciz "low_base_pmls"
.quad make_pipe
.asciz "make_pipe"
.quad make_process_ready
.asciz "make_process_ready"
.quad make_unix_pipe
.asciz "make_unix_pipe"
.quad malloc
.asciz "malloc"
.quad map_vfs_directory
.asciz "map_vfs_directory"
.quad mboot2_find_next
.asciz "mboot2_find_next"
.quad mboot2_find_tag
.asciz "mboot2_find_tag"
.quad mboot_is_2
.asciz "mboot_is_2"
.quad mboot_struct
.asciz "mboot_struct"
.quad mboot_unmark_valid_memory
.asciz "mboot_unmark_valid_memory"
.quad memchr
.asciz "memchr"
.quad memcmp
.asciz "memcmp"
.quad memcpy
.asciz "memcpy"
.quad memmove
.asciz "memmove"
.quad memrchr
.asciz "memrchr"
.quad memset
.asciz "memset"
.quad memsetw
.asciz "memsetw"
.quad mkdir_fs
.asciz "mkdir_fs"
.quad mmu_allocate_a_frame
.asciz "mmu_allocate_a_frame"
.quad mmu_allocate_n_frames
.asciz "mmu_allocate_n_frames"
.quad mmu_clone
.asciz "mmu_clone"
.quad mmu_copy_on_write
.asciz "mmu_copy_on_write"
.quad mmu_count_shm
.asciz "mmu_count_shm"
.quad mmu_count_user
.asciz "mmu_count_user"
.quad mmu_first_frame
.asciz "mmu_first_frame"
.quad mmu_first_n_frames
.asciz "mmu_first_n_frames"
.quad mmu_frame_allocate
.asciz "mmu_frame_allocate"
.quad mmu_frame_clear
.asciz "mmu_frame_clear"
.quad mmu_frame_map_address
.asciz "mmu_frame_map_address"
.quad mmu_frame_release
.asciz "mmu_frame_release"
.quad mmu_frame_set
.asciz "mmu_frame_set"
.quad mmu_frame_test
.asciz "mmu_frame_test"
.quad mmu_free
.asciz "mmu_free"
.quad mmu_get_kernel_directory
.asciz "mmu_get_kernel_directory"
.quad mmu_get_page
.asciz "mmu_get_page"
.quad mmu_get_page_deep
.asciz "mmu_get_page_deep"
.quad mmu_get_page_other
.asciz "mmu_get_page_other"
.quad mmu_init
.asciz "mmu_init"
.quad mmu_invalidate
.asciz "mmu_invalidate"
.quad mmu_map_from_physical
.asciz "mmu_map_from_physical"
.quad mmu_map_mmio_region
.asciz "mmu_map_mmio_region"
.quad mmu_map_module
.asciz "mmu_map_module"
.quad mmu_map_to_physical
.asciz "mmu_map_to_physical"
.quad mmu_set_directory
.asciz "mmu_set_directory"
.quad mmu_total_memory
.asciz "mmu_total_memory"
.quad mmu_unmap_module
.asciz "mmu_unmap_module"
.quad mmu_unmap_user
.asciz "mmu_unmap_user"
.quad mmu_used_memory
.asciz "mmu_used_memory"
.quad mmu_validate_user_pointer
.asciz "mmu_validate_user_pointer"
.quad modules_get_list
.asciz "modules_get_list"
.quad modules_install
.asciz "modules_install"
.quad mount_multiboot_ramdisks
.asciz "mount_multiboot_ramdisks"
.quad mutex_acquire
.asciz "mutex_acquire"
.quad mutex_init
.asciz "mutex_init"
.quad mutex_release
.asciz "mutex_release"
.quad net_accept
.asciz "net_accept"
.quad net_add_interface
.asciz "net_add_interface"
.quad net_arp_ask
.asciz "net_arp_ask"
.quad net_arp_cache
.asciz "net_arp_cache"
.quad net_arp_cache_add
.asciz "net_arp_cache_add"
.quad net_arp_cache_get
.asciz "net_arp_cache_get"
.quad net_arp_cache_lock
.asciz "net_arp_cache_lock"
.quad net_arp_handle
.asciz "net_arp_handle"
.quad net_bind
.asciz "net_bind"
.quad net_connect
.asciz "net_connect"
.quad net_eth_handle
.asciz "net_eth_handle"
.quad net_eth_send
.asciz "net_eth_send"
.quad net_getpeername
.asciz "net_getpeername"
.quad net_getsockname
.asciz "net_getsockname"
.quad net_getsockopt
.asciz "net_getsockopt"
.quad net_if_any
.asciz "net_if_any"
.quad net_if_lookup
.asciz "net_if_lookup"
.quad net_if_route
.asciz "net_if_route"
.quad net_install
.asciz "net_install"
.quad net_ipv4_handle
.asciz "net_ipv4_handle"
.quad net_ipv4_send
.asciz "net_ipv4_send"
.quad net_ipv4_socket
.asciz "net_ipv4_socket"
.quad net_listen
.asciz "net_listen"
.quad net_raw_socket
.asciz "net_raw_socket"
.quad net_raw_sockets_list
.asciz "net_raw_sockets_list"
.quad net_raw_sockets_lock
.asciz "net_raw_sockets_lock"
.quad net_recv
.asciz "net_recv"
.quad net_send
.asciz "net_send"
.quad net_setsockopt
.asciz "net_setsockopt"
.quad net_shutdown
.asciz "net_shutdown"
.quad net_so_socket
.asciz "net_so_socket"
.quad net_sock_add
.asciz "net_sock_add"
.quad net_sock_alert
.asciz "net_sock_alert"
.quad net_sock_create
.asciz "net_sock_create"
.quad net_sock_get
.asciz "net_sock_get"
.quad net_socket
.asciz "net_socket"
.quad next_ready_process
.asciz "next_ready_process"
.quad now
.asciz "now"
.quad open_fs
.asciz "open_fs"
.quad open_pipe
.asciz "open_pipe"
.quad open_pty_master
.asciz "open_pty_master"
.quad open_pty_slave
.asciz "open_pty_slave"
.quad outportb
.asciz "outportb"
.quad outportl
.asciz "outportl"
.quad outports
.asciz "outports"
.quad outportsm
.asciz "outportsm"
.quad packetfs_initialize
.asciz "packetfs_initialize"
.quad pat_initialize
.asciz "pat_initialize"
.quad pci_find_type
.asciz "pci_find_type"
.quad pci_get_interrupt
.asciz "pci_get_interrupt"
.quad pci_read_field
.asciz "pci_read_field"
.quad pci_scan
.asciz "pci_scan"
.quad pci_scan_bus
.asciz "pci_scan_bus"
.quad pci_scan_func
.asciz "pci_scan_func"
.quad pci_scan_slot
.asciz "pci_scan_slot"
.quad pci_write_field
.asciz "pci_write_field"
.quad pcie_ecam_phys
.asciz "pcie_ecam_phys"
.quad phys
.asciz "phys"
.quad pic_initialize
.asciz "pic_initialize"
.quad pipe_destroy
.asciz "pipe_destroy"
.quad pipe_size
.asciz "pipe_size"
.quad pipe_unsize
.asciz "pipe_unsize"
.quad pit_initialize
.asciz "pit_initialize"
.quad pit_interrupt
.asciz "pit_interrupt"
.quad portio_initialize
.asciz "portio_initialize"
.quad printf
.asciz "printf"
.quad printf_output
.asciz "printf_output"
.quad process_alert_node
.asciz "process_alert_node"
.quad process_alert_node_locked
.asciz "process_alert_node_locked"
.quad process_append_fd
.asciz "process_append_fd"
.quad process_awaken_from_fswait
.asciz "process_awaken_from_fswait"
.quad process_awaken_signal
.asciz "process_awaken_signal"
.quad process_check_signals
.asciz "process_check_signals"
.quad process_compare
.asciz "process_compare"
.quad process_delete
.asciz "process_delete"
.quad process_from_pid
.asciz "process_from_pid"
.quad process_get_parent
.asciz "process_get_parent"
.quad process_is_ready
.asciz "process_is_ready"
.quad process_list
.asciz "process_list"
.quad process_move_fd
.asciz "process_move_fd"
.quad process_queue
.asciz "process_queue"
.quad process_reap
.asciz "process_reap"
.quad process_reap_later
.asciz "process_reap_later"
.quad process_release_directory
.asciz "process_release_directory"
.quad process_timeout_sleep
.asciz "process_timeout_sleep"
.quad process_tree
.asciz "process_tree"
.quad process_wait_nodes
.asciz "process_wait_nodes"
.quad processor_count
.asciz "processor_count"
.quad processor_local_data
.asciz "processor_local_data"
.quad procfs_initialize
.asciz "procfs_initialize"
.quad procfs_install
.asciz "procfs_install"
.quad procfs_printf
.asciz "procfs_printf"
.quad ps2_mouse_alternate
.asciz "ps2_mouse_alternate"
.quad ps2hid_install
.asciz "ps2hid_install"
.quad ptr_validate
.asciz "ptr_validate"
.quad ptrace_attach
.asciz "ptrace_attach"
.quad ptrace_continue
.asciz "ptrace_continue"
.quad ptrace_detach
.asciz "ptrace_detach"
.quad ptrace_getregs
.asciz "ptrace_getregs"
.quad ptrace_handle
.asciz "ptrace_handle"
.quad ptrace_peek
.asciz "ptrace_peek"
.quad ptrace_poke
.asciz "ptrace_poke"
.quad ptrace_self
.asciz "ptrace_self"
.quad ptrace_signal
.asciz "ptrace_signal"
.quad ptrace_signals_only
.asciz "ptrace_signals_only"
.quad ptrace_singlestep
.asciz "ptrace_singlestep"
.quad pty_available_input
.asciz "pty_available_input"
.quad pty_available_output
.asciz "pty_available_output"
.quad pty_create
.asciz "pty_create"
.quad pty_install
.asciz "pty_install"
.quad pty_ioctl
.asciz "pty_ioctl"
.quad pty_master_create
.asciz "pty_master_create"
.quad pty_new
.asciz "pty_new"
.quad pty_slave_create
.asciz "pty_slave_create"
.quad ramdisk_mount
.asciz "ramdisk_mount"
.quad rand
.asciz "rand"
.quad random_initialize
.asciz "random_initialize"
.quad read_cmos
.asciz "read_cmos"
.quad read_fs
.asciz "read_fs"
.quad read_pipe
.asciz "read_pipe"
.quad read_pty_master
.asciz "read_pty_master"
.quad read_pty_slave
.asciz "read_pty_slave"
.quad readdir_fs
.asciz "readdir_fs"
.quad readlink_fs
.asciz "readlink_fs"
.quad realloc
.asciz "realloc"
.quad reap_queue
.asciz "reap_queue"
.quad refcount_dec
.asciz "refcount_dec"
.quad refcount_inc
.asciz "refcount_inc"
.quad relative_time
.asciz "relative_time"
.quad return_from_signal_handler
.asciz "return_from_signal_handler"
.quad rfind
.asciz "rfind"
.quad ring_buffer_alert_waiters
.asciz "ring_buffer_alert_waiters"
.quad ring_buffer_available
.asciz "ring_buffer_available"
.quad ring_buffer_create
.asciz "ring_buffer_create"
.quad ring_buffer_destroy
.asciz "ring_buffer_destroy"
.quad ring_buffer_eof
.asciz "ring_buffer_eof"
.quad ring_buffer_interrupt
.asciz "ring_buffer_interrupt"
.quad ring_buffer_read
.asciz "ring_buffer_read"
.quad ring_buffer_select_wait
.asciz "ring_buffer_select_wait"
.quad ring_buffer_size
.asciz "ring_buffer_size"
.quad ring_buffer_unread
.asciz "ring_buffer_unread"
.quad ring_buffer_write
.asciz "ring_buffer_write"
.quad sbrk
.asciz "sbrk"
.quad selectcheck_fs
.asciz "selectcheck_fs"
.quad selectwait_fs
.asciz "selectwait_fs"
.quad send_signal
.asciz "send_signal"
.quad serial_handler_ac
.asciz "serial_handler_ac"
.quad serial_handler_bd
.asciz "serial_handler_bd"
.quad serial_initialize
.asciz "serial_initialize"
.quad settimeofday
.asciz "settimeofday"
.quad shm_install
.asciz "shm_install"
.quad shm_obtain
.asciz "shm_obtain"
.quad shm_release
.asciz "shm_release"
.quad shm_release_all
.asciz "shm_release_all"
.quad shm_tree
.asciz "shm_tree"
.quad signal_await
.asciz "signal_await"
.quad sleep_on
.asciz "sleep_on"
.quad sleep_on_unlocking
.asciz "sleep_on_unlocking"
.quad sleep_queue
.asciz "sleep_queue"
.quad sleep_until
.asciz "sleep_until"
.quad smp_initialize
.asciz "smp_initialize"
.quad snd_install
.asciz "snd_install"
.quad snd_register
.asciz "snd_register"
.quad snd_request_buf
.asciz "snd_request_buf"
.quad snd_unregister
.asciz "snd_unregister"
.quad snprintf
.asciz "snprintf"
.quad sock_generic_check
.asciz "sock_generic_check"
.quad sock_generic_close
.asciz "sock_generic_close"
.quad sock_generic_ioctl
.asciz "sock_generic_ioctl"
.quad sock_generic_wait
.asciz "sock_generic_wait"
.quad sock_tcp_getpeername
.asciz "sock_tcp_getpeername"
.quad sock_tcp_getsockname
.asciz "sock_tcp_getsockname"
.quad sock_tcp_read
.asciz "sock_tcp_read"
.quad sock_tcp_write
.asciz "sock_tcp_write"
.quad spawn_init
.asciz "spawn_init"
.quad spawn_kidle
.asciz "spawn_kidle"
.quad spawn_process
.asciz "spawn_process"
.quad spawn_worker_thread
.asciz "spawn_worker_thread"
.quad stack_top
.asciz "stack_top"
.quad start
.asciz "start"
.quad startswith
.asciz "startswith"
.quad stpcpy
.asciz "stpcpy"
.quad strchr
.asciz "strchr"
.quad strchrnul
.asciz "strchrnul"
.quad strcmp
.asciz "strcmp"
.quad strcpy
.asciz "strcpy"
.quad strcspn
.asciz "strcspn"
.quad strdup
.asciz "strdup"
.quad strlen
.asciz "strlen"
.quad strpbrk
.asciz "strpbrk"
.quad strrchr
.asciz "strrchr"
.quad strspn
.asciz "strspn"
.quad strstr
.asciz "strstr"
.quad strtok_r
.asciz "strtok_r"
.quad switch_next
.asciz "switch_next"
.quad switch_task
.asciz "switch_task"
.quad symlink_fs
.asciz "symlink_fs"
.quad sys_access
.asciz "sys_access"
.quad sys_chdir
.asciz "sys_chdir"
.quad sys_chmod
.asciz "sys_chmod"
.quad sys_chown
.asciz "sys_chown"
.quad sys_clone
.asciz "sys_clone"
.quad sys_close
.asciz "sys_close"
.quad sys_dup2
.asciz "sys_dup2"
.quad sys_execve
.asciz "sys_execve"
.quad sys_exit
.asciz "sys_exit"
.quad sys_fork
.asciz "sys_fork"
.quad sys_fswait
.asciz "sys_fswait"
.quad sys_fswait_multi
.asciz "sys_fswait_multi"
.quad sys_fswait_timeout
.asciz "sys_fswait_timeout"
.quad sys_getcwd
.asciz "sys_getcwd"
.quad sys_getegid
.asciz "sys_getegid"
.quad sys_geteuid
.asciz "sys_geteuid"
.quad sys_getgid
.asciz "sys_getgid"
.quad sys_getgroups
.asciz "sys_getgroups"
.quad sys_gethostname
.asciz "sys_gethostname"
.quad sys_getpgid
.asciz "sys_getpgid"
.quad sys_getpid
.asciz "sys_getpid"
.quad sys_gettid
.asciz "sys_gettid"
.quad sys_gettimeofday
.asciz "sys_gettimeofday"
.quad sys_getuid
.asciz "sys_getuid"
.quad sys_ioctl
.asciz "sys_ioctl"
.quad sys_kill
.asciz "sys_kill"
.quad sys_lstat
.asciz "sys_lstat"
.quad sys_mkdir
.asciz "sys_mkdir"
.quad sys_mount
.asciz "sys_mount"
.quad sys_open
.asciz "sys_open"
.quad sys_openpty
.asciz "sys_openpty"
.quad sys_pipe
.asciz "sys_pipe"
.quad sys_read
.asciz "sys_read"
.quad sys_readdir
.asciz "sys_readdir"
.quad sys_readlink
.asciz "sys_readlink"
.quad sys_reboot
.asciz "sys_reboot"
.quad sys_sbrk
.asciz "sys_sbrk"
.quad sys_seek
.asciz "sys_seek"
.quad sys_setgid
.asciz "sys_setgid"
.quad sys_setgroups
.asciz "sys_setgroups"
.quad sys_sethostname
.asciz "sys_sethostname"
.quad sys_setpgid
.asciz "sys_setpgid"
.quad sys_setsid
.asciz "sys_setsid"
.quad sys_settimeofday
.asciz "sys_settimeofday"
.quad sys_setuid
.asciz "sys_setuid"
.quad sys_shm_obtain
.asciz "sys_shm_obtain"
.quad sys_shm_release
.asciz "sys_shm_release"
.quad sys_sigaction
.asciz "sys_sigaction"
.quad sys_signal
.asciz "sys_signal"
.quad sys_sigpending
.asciz "sys_sigpending"
.quad sys_sigprocmask
.asciz "sys_sigprocmask"
.quad sys_sigsuspend_cur
.asciz "sys_sigsuspend_cur"
.quad sys_sigwait
.asciz "sys_sigwait"
.quad sys_sleep
.asciz "sys_sleep"
.quad sys_sleepabs
.asciz "sys_sleepabs"
.quad sys_stat
.asciz "sys_stat"
.quad sys_statf
.asciz "sys_statf"
.quad sys_symlink
.asciz "sys_symlink"
.quad sys_sysfunc
.asciz "sys_sysfunc"
.quad sys_times
.asciz "sys_times"
.quad sys_umask
.asciz "sys_umask"
.quad sys_uname
.asciz "sys_uname"
.quad sys_unlink
.asciz "sys_unlink"
.quad sys_waitpid
.asciz "sys_waitpid"
.quad sys_write
.asciz "sys_write"
.quad sys_yield
.asciz "sys_yield"
.quad syscall_handler
.asciz "syscall_handler"
.quad system
.asciz "system"
.quad tarfs_register_init
.asciz "tarfs_register_init"
.quad task_exit
.asciz "task_exit"
.quad tasking_start
.asciz "tasking_start"
.quad tmpfs_create
.asciz "tmpfs_create"
.quad tmpfs_mount
.asciz "tmpfs_mount"
.quad tmpfs_register_init
.asciz "tmpfs_register_init"
.quad tokenize
.asciz "tokenize"
.quad tree_break_off
.asciz "tree_break_off"
.quad tree_count_children
.asciz "tree_count_children"
.quad tree_create
.asciz "tree_create"
.quad tree_destroy
.asciz "tree_destroy"
.quad tree_find
.asciz "tree_find"
.quad tree_find_parent
.asciz "tree_find_parent"
.quad tree_free
.asciz "tree_free"
.quad tree_node_create
.asciz "tree_node_create"
.quad tree_node_destroy
.asciz "tree_node_destroy"
.quad tree_node_find
.asciz "tree_node_find"
.quad tree_node_find_parent
.asciz "tree_node_find_parent"
.quad tree_node_free
.asciz "tree_node_free"
.quad tree_node_insert_child
.asciz "tree_node_insert_child"
.quad tree_node_insert_child_node
.asciz "tree_node_insert_child_node"
.quad tree_node_parent_remove
.asciz "tree_node_parent_remove"
.quad tree_node_remove
.asciz "tree_node_remove"
.quad tree_remove
.asciz "tree_remove"
.quad tree_remove_reparent_root
.asciz "tree_remove_reparent_root"
.quad tree_set_root
.asciz "tree_set_root"
.quad truncate_fs
.asciz "truncate_fs"
.quad tsc_basis_time
.asciz "tsc_basis_time"
.quad tsc_mhz
.asciz "tsc_mhz"
.quad tty_input_process
.asciz "tty_input_process"
.quad tty_output_process
.asciz "tty_output_process"
.quad tty_output_process_slave
.asciz "tty_output_process_slave"
.quad twom_high_pds
.asciz "twom_high_pds"
.quad unlink_fs
.asciz "unlink_fs"
.quad update_process_times
.asciz "update_process_times"
.quad update_process_usage
.asciz "update_process_usage"
.quad valloc
.asciz "valloc"
.quad vfs_install
.asciz "vfs_install"
.quad vfs_lock
.asciz "vfs_lock"
.quad vfs_mount
.asciz "vfs_mount"
.quad vfs_mount_type
.asciz "vfs_mount_type"
.quad vfs_register
.asciz "vfs_register"
.quad vsnprintf
.asciz "vsnprintf"
.quad waitpid
.asciz "waitpid"
.quad wakeup_queue
.asciz "wakeup_queue"
.quad wakeup_queue_interrupted
.asciz "wakeup_queue_interrupted"
.quad wakeup_queue_one
.asciz "wakeup_queue_one"
.quad wakeup_sleepers
.asciz "wakeup_sleepers"
.quad write_fs
.asciz "write_fs"
.quad write_pipe
.asciz "write_pipe"
.quad write_pty_master
.asciz "write_pty_master"
.quad write_pty_slave
.asciz "write_pty_slave"
.quad xtoi
.asciz "xtoi"
.quad xvasprintf
.asciz "xvasprintf"
.quad zero_initialize
.asciz "zero_initialize"
.global kernel_symbols_end
kernel_symbols_end:
