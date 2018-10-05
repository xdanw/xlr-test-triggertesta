
print "*** testTriggerA init *** \r\n";

print "triggerState_pre: " + triggerState;

# If empty, set to 0
if triggerState == "":
    triggerState = "0";
    print "set > 0";

# else: ... nah, for testing let's increment to 1 on the first run
if int(triggerState) >= 0:
    triggerState = str(int(triggerState)+1);
    print "set > " + str(int(triggerState)) + "+1=" + str(int(triggerState)+1);

print "triggerState_post: " + triggerState;
