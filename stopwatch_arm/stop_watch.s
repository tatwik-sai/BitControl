.syntax unified
.cpu cortex-m0
.thumb

.section .text
.global __main
.extern __use_two_region_memory

LED_DIRSET_ADDR:   .word 0x50000518
LED_OUTSET_ADDR:   .word 0x50000508
LED_OUTCLR_ADDR:   .word 0x5000050C
BUTTON_A_ADDR:     .word 0x50000014
BUTTON_B_ADDR:     .word 0x50000016

TIMER0_START_ADDR: .word 0x40008000
TIMER0_STOP_ADDR:  .word 0x40008004
TIMER0_CLEAR_ADDR: .word 0x4000800C
TIMER0_VAL_ADDR:   .word 0x40008540

@ Time tracking variables
.section .bss
.align 4
seconds:       .space 4
minutes:       .space 4
current_state: .space 4
button_state:  .space 4

@ LED patterns for digits 0-9
.section .rodata
.align 4
digit_0: .word 0x1F11F  @ 0
digit_1: .word 0x04444  @ 1
digit_2: .word 0x1F88F  @ 2
digit_3: .word 0x1F11F  @ 3
digit_4: .word 0x11F11  @ 4
digit_5: .word 0xF88F   @ 5
digit_6: .word 0x1F88F  @ 6
digit_7: .word 0x1F11F  @ 7
digit_8: .word 0x11F11  @ 8
digit_9: .word 0xF88F   @ 9

.section .text
__main:
    ldr r0, =0x20004000
    mov sp, r0

    ldr r0, LED_BASE_VAL
    ldr r1, LED_DIRSET_OFF
    adds r0, r0, r1
    ldr r1, =0x1FFFF   @ Set all LED pins as output
    str r1, [r0]

    @ Initialize timer
    bl init_timer
    bl clear_display
    movs r0, #0
    ldr r1, =current_state
    str r0, [r1]
    ldr r1, =button_state
    str r0, [r1]

main_loop:
    bl check_buttons
    
    @ Update timer display based on current state
    ldr r0, =current_state
    ldr r0, [r0]
    cmp r0, #0
    beq timer_stopped
    cmp r0, #1
    beq timer_running
    b main_loop

timer_stopped:
    bl display_time
    b main_loop

timer_running:
    bl update_time
    bl display_time
    ldr r0, =100000
    bl delay
    b main_loop

@ Initialize timer
init_timer:
    push {lr}
    ldr r0, TIMER0_BASE_VAL
    ldr r1, TIMER0_CLEAR_OFF
    adds r0, r0, r1
    movs r1, #1
    str r1, [r0]    @ Clear timer
    pop {pc}

@ Start the timer
start_timer:
    push {lr}
    ldr r0, TIMER0_BASE_VAL
    ldr r1, TIMER0_START_OFF
    adds r0, r0, r1
    movs r1, #1
    str r1, [r0]
    pop {pc}

@ Stop the timer
stop_timer:
    push {lr}
    ldr r0, TIMER0_BASE_VAL
    ldr r1, TIMER0_STOP_OFF
    adds r0, r0, r1
    movs r1, #1
    str r1, [r0]   
    pop {pc}


clear_display:
    push {lr}
    ldr r0, LED_BASE_VAL
    ldr r1, LED_OUTCLR_OFF
    adds r0, r0, r1
    ldr r1, =0x1FFFF   @ Clear all LEDs
    str r1, [r0]
    pop {pc}

@ Check button inputs
check_buttons:
    push {r4, r5, lr}
    
    ldr r0, LED_BASE_VAL
    ldr r1, BUTTON_A_OFF
    adds r0, r0, r1
    ldr r4, [r0]   
    
    ldr r0, LED_BASE_VAL
    ldr r1, BUTTON_B_OFF
    adds r0, r0, r1
    ldr r5, [r0] 
    
    @ Check if button A pressed (start/stop)
    ldr r0, =button_state
    ldr r1, [r0]
    cmp r4, #0
    beq .button_A_not_pressed
    cmp r1, #0
    bne .skip_button_A
    movs r1, #1
    str r1, [r0]     

    ldr r0, =current_state
    ldr r1, [r0]
    cmp r1, #0
    bne .stop_state
    movs r1, #1
    str r1, [r0]   
    bl start_timer
    b .skip_button_A
    
.stop_state:
    movs r1, #0
    str r1, [r0]   
    bl stop_timer
    b .skip_button_A
    
.button_A_not_pressed:
    movs r1, #0
    ldr r0, =button_state
    str r1, [r0]  
    
.skip_button_A:
    cmp r5, #0
    beq .button_B_not_pressed
    
    @ Reset timer
    ldr r0, =seconds
    movs r1, #0
    str r1, [r0]
    ldr r0, =minutes
    str r1, [r0]
    
    @ Clear timer
    bl init_timer
    
.button_B_not_pressed:
    pop {r4, r5, pc}

@ Update timer values
update_time:
    push {r4, r5, lr}
    
    ldr r0, TIMER0_BASE_VAL
    ldr r1, TIMER0_VAL_OFF
    adds r0, r0, r1
    ldr r0, [r0] 
    
    ldr r1, =1000000
    bl divide_unsigned
    ldr r4, =seconds
    ldr r5, [r4]
    cmp r5, r0
    beq .skip_update
    
    str r0, [r4] 
    
    cmp r0, #60
    blt .skip_update
    
    @ Seconds reached 60, increment minutes
    movs r0, #0
    str r0, [r4]    @ Reset seconds
    
    ldr r4, =minutes
    ldr r0, [r4]
    adds r0, r0, #1
    str r0, [r4]    @ Increment minutes
    
.skip_update:
    pop {r4, r5, pc}

display_time:
    push {r4, r5, r6, r7, lr}

    bl clear_display
    
    ldr r4, =seconds
    ldr r4, [r4]    
    ldr r5, =minutes
    ldr r5, [r5]
    
    movs r0, r4
    movs r1, #10
    bl divide_unsigned
    movs r6, r0    
    
    movs r0, r4  
    movs r1, r6     
    movs r2, #10
    muls r1, r2     
    subs r7, r0, r1
    
    movs r0, r5
    movs r1, #10
    bl divide_unsigned
    movs r4, r0     
    
    movs r0, r5    
    movs r1, r4     
    movs r2, #10
    muls r1, r2     
    subs r5, r0, r1
    
    @ Display each digit
    movs r0, r5     
    movs r1, #0     
    bl display_digit
    
    movs r0, r4   
    movs r1, #1  
    bl display_digit
    
    movs r0, r6     
    movs r1, #2     
    bl display_digit
    
    movs r0, r7     
    movs r1, #3     
    bl display_digit
    
    pop {r4, r5, r6, r7, pc}

divide_unsigned:
    push {r2, r3, r4, lr}
    
    cmp r1, #0
    beq .div_by_zero
    
    movs r2, #0  
    movs r3, #0     
    movs r4, #32    
    
.div_loop:

    lsls r0, r0, #1
    adcs r3, r3, r3  
    
    cmp r3, r1
    blt .div_skip

    subs r3, r3, r1
    
    adds r2, r2, #1
    
.div_skip:
    lsls r2, r2, #1
    
    subs r4, r4, #1
    bne .div_loop
    

    lsrs r2, r2, #1
    movs r0, r2     
    
    pop {r2, r3, r4, pc}
    
.div_by_zero:
    movs r0, #0
    subs r0, r0, #1  
    pop {r2, r3, r4, pc}

@ Display a digit at a specified position
display_digit:
    push {r4, r5, lr}

    cmp r0, #9
    bls .valid_digit
    movs r0, #0     
    
.valid_digit:

    movs r2, r0
    ldr r0, =digit_table  
    lsls r2, r2, #2      
    adds r0, r0, r2      
    ldr r0, [r0]         
    ldr r2, [r0]         
    
    lsls r1, r1, #3    
    lsls r2, r2, r1     
    
    @ Set LEDs for this digit
    ldr r0, LED_BASE_VAL
    ldr r3, LED_OUTSET_OFF
    adds r0, r0, r3
    str r2, [r0]         @ Display digit
    
    pop {r4, r5, pc}

@ Simple delay function
delay:
    subs r0, r0, #1
    bne delay
    bx lr

@ Digit pattern lookup table
.align 4
digit_table:
    .word digit_0
    .word digit_1
    .word digit_2
    .word digit_3
    .word digit_4
    .word digit_5
    .word digit_6
    .word digit_7
    .word digit_8
    .word digit_9
