import src.actions as actions

testaction = actions.actions()
testaction.addAction(
    actionName="switch to starting scene",
    actionProvider="obs",
    actionData="sceneswitch-17",
    group="scenes",
    state="",
    label="Starting",
    icon="",
    buttonlocation="deck",
)
testaction.addAction(
    actionName="test thingy",
    actionProvider="exampleextension",
    actionData="a good action data set",
    group="scenes",
    state="",
    label="test thingy",
    icon="",
    buttonlocation="deck",
)
