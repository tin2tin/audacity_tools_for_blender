import bpy

from .. import pipe_utilities


class SEQUENCER_OT_record_in_audacity(bpy.types.Operator):
    """Record Audacity"""

    bl_idname = "sequencer.record_in_audacity"
    bl_label = "Record in Audacity"
    bl_description = "Record in Audacity"
    bl_category = "Audacity Tools"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.window_manager.audacity_tools_pipe_available

    def execute(self, context):
        # check if pipe available
        if not pipe_utilities.check_pipe():
            self.report({"WARNING"}, "No pipe available, try refresh operator")
            return {"FINISHED"}

        if not bpy.context.scene.sequence_editor:
            bpy.context.scene.sequence_editor_create()
        scene = bpy.context.scene
        props = scene.audacity_tools_props
        sequence = scene.sequence_editor

        props.record_start = scene.frame_current
        props.record_end = -1
        bpy.context.scene.use_audio = True

        pipe_utilities.do_command("SelectAll")
        pipe_utilities.do_command("RemoveTracks")

        pipe_utilities.do_command("Record1stChoice:")
        bpy.ops.screen.animation_play()

        return {"FINISHED"}


### REGISTER ---

def register():
    bpy.utils.register_class(SEQUENCER_OT_record_in_audacity)

def unregister():
    bpy.utils.unregister_class(SEQUENCER_OT_record_in_audacity)