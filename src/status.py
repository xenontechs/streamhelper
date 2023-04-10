import sys
import src.datastore as data
import src.obs as obs
import flask
import jinja2


class status:
    def __init__(self) -> None:
        # config
        # obs connection
        # obs status (streaming, ...)
        self.obsStatus = self.obsStatus()
        self.obsStats = self.obsStats()
        self.selfStatus = self.selfStatus()
        # obs presets (profile, scenes, reqs?)
        # other apps status (streamerbot running & connected, spotify currentsong)
        # mappings (buttons to scenes)
        #

    def update(self, key=""):
        updates = {}
        if key == "" or key == "config":
            # get status of config file (file found, errors?)
            print("statusupdate: config")
        if key == "" or key == "obsStatus":
            print("statusupdate: obsStatus")
            updates = updates | self.obsStatus.update().__dict__
        if key == "" or key == "obsStats":
            print("statusupdate: obsStats")
            updates = updates | self.obsStats.update().__dict__

        return updates

    class obsStatus:
        def __init__(self) -> None:
            self.obsVersion = ""
            self.obsWebSocketVersion = ""
            self.rpcVersion = ""
            self.availableRequests = []
            self.supportedImageFormats = []
            self.platform = ""
            self.platformDescription = ""

        def update(self):
            update = obs.gen.getVersion()
            self.obsVersion = update.obs_version
            self.obsWebSocketVersion = update.obs_web_socket_version
            self.rpcVersion = update.rpc_version
            self.availableRequests = update.available_requests
            self.supportedImageFormats = update.supported_image_formats
            self.platform = update.platform
            self.platformDescription = update.platform_description
            return self

    class obsStats:
        def __init__(self) -> None:
            self.cpuUsage = 0
            self.memoryUsage = 0
            self.availableDiskSpace = 0
            self.activeFps = 0
            self.averageFrameRenderTime = 0
            self.renderSkippedFrames = 0
            self.renderTotalFrames = 0
            self.outputSkippedFrames = 0
            self.outputTotalFrames = 0
            self.webSocketSessionIncomingMessages = 0
            self.webSocketSessionOutgoingMessages = 0

        def update(self):
            update = obs.gen.getStats()
            self.cpuUsage = update.cpu_usage
            self.memoryUsage = update.memory_usage
            self.availableDiskSpace = update.available_disk_space
            self.activeFps = update.active_fps
            self.averageFrameRenderTime = update.average_frame_render_time
            self.renderSkippedFrames = update.render_skipped_frames
            self.renderTotalFrames = update.render_total_frames
            self.outputSkippedFrames = update.output_skipped_frames
            self.outputTotalFrames = update.output_total_frames
            self.webSocketSessionIncomingMessages = update.web_socket_session_incoming_messages
            self.webSocketSessionOutgoingMessages = update.web_socket_session_outgoing_messages
            return self

    class selfStatus:
        def __init__(self) -> None:
            self.python = sys.version
            self.flask = flask.__version__
            self.jinja2 = jinja2.__version__
