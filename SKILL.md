# Skill: Interacting with Overlord MCP

## Overview
This skill explains how to use the tools exposed by the Overlord MCP server and how to retrieve information in an authorized penetration testing or remote management scenario.

## Core Rules for the Agent
1. **Never guess tool parameters:** Always inspect the tool schema provided by the MCP server via the handshake/discovery phase before calling a tool.
2. **Format strictly in JSON:** Pass arguments matching the exact parameter types and structures specified in the tool definition.
3. **Handle errors gracefully:** If an MCP tool execution fails or returns an error payload, parse the error message, inform the user, and propose a corrective action rather than looping blindly.

## Workflow Instructions

### Query client information
* Any requests for agent metrics, statistics, or general information applies here.
* **/clients/banned-ips** returns a list of banned IP addresses.
* **/clients/countries** returns a list of two-letter country codes and count.
* **/enrollment/stats** shows statistics of the agents that have been enrolled.
* **/metrics** lists dashboard data including number of agents, agent connection status, OS, country, total connections, command statistics, sessions, bandwidth, and ping with timestamp in epoch time. Also includes server status.

### Query user information
* **/auth/me** returns general information for the current user. This can be used to verify the agent's permissions and access level.
* **/groups** has not been documented.
* **/login/branding** returns various graphic and branding data.
* **/registration/status** returns the current registration settings and password policy.
* **/users/{userId}/client-access** returns 'allow' for the access parameter if the user is allowed to access agents and 'deny' if not.
* /**users/{userId}/effective-permissions** returns a list of the effective permissions that the user has been granted.
* **/users/{userId}/extra-permissions** returns a list of extra permissions that the user has been granted.
* **/users/{userId}/permission-groups** returns the groupIds for the permission groups that the user belongs to.

### Query server information
* **/auto-deploys** returns a list of the executable files that are set to deploy automatically when an agent connects.
* **/auto-scripts** returns a list of the scripts that are set to execute automatically when an agent connects.
* **/build/list** returns a list of the agent builds that have been created.
* **/build/macos-sdk/status** returns the status of the macOS SDK.
* **/build/plugins** returns a list of the plugins that are available for building agent executables.
* **/build/profiles** returns a list of preset profiles for building agent executables.
* **/cert/info** shows the source of the server's TLS certificate.'
* **/logs** returns server logs about agent connections.
* **/mfa/status** returns the status of multi-factor authentication for the current user.
* **/notifications/ws** used to retrieve notiifications over a websocket.
* **/notifications/config** returns notification settings.
    - **minIntervalMs:** The minimum interval in milliseconds
    - **spamWindowMs:**  The spam window in milliseconds
    - **spamWarnThreshold:** The spam warning threshold
    - **historyLimit:** Max number of history items to hold
    - **webhookEnabled:** Returns true if a webhook is enabled and false if not.
    - **webhookUrl:** Shows the webhook URL
    - **telegramEnabled:** Returns true if Telegram notifications are enabled and false if not.
    - **telegramBotToken:** Shows the Telegram bot token.
    - **telegramChatId:** Shows the Telegram Chat ID.
    - **clipboardEnabled:** Returns true if clipboard alerts are enabled and false if not.
    - **antiSpamMaxHits:** Show the maximum number of times that a notification for a specific keyword will be shown.
    - **antiSpamWindowMs:** The length of a window in milliseconds for the anti-spam limits.
    - **antiSpamCooldownMs:** The length of time in milliseconds that the notifications will be paused for a keyword after hitting the anti-spam limit.
* **/notifications/{notificationId}/screenshot** returns a screenshot for a specific notification.
* **/notifications/my-settings** retrieves notification settings.
    - **Settings:**
        - **webhook_enabled:** Returns 1 if enabled and 0 if not.
        - **webhook_url:** Returns webhook URL.
        - **webhook_template:** Returns webhook template.
        - **telegram_enabled:** Returns 1 if Telegram notifications are enabled and 0 if not.
        - **telegram_bot_token:** Returns Telegram bot token.
        - **telegram_chat_id:** Returns Telegram chat ID.
        - **telegram_template:** Returns Telegram template.
        - **client_event_webhook:** Returns 1 if the webhook client event delivery channel is enabled and 0 if not.
        - **client_event_telegram:** Returns 1 if the Telegram client event delivery channel is enabled and 0 if not.
        - **client_event_push:** Returns 1 if the push notification client event delivery channel is enabled and 0 if not. 
    - **Defaults:** Returns default templates for webhooks and Telegram.
* **/permissions** returns a list of available permissions.
    - **id:**
        - **users:manage:** Manage users and roles
        - **clients:control:** Control clients (execute commands, desktop, console, files)
        - **clients:build:** Build client binaries
        - **clients:enroll:** Manage client enrollment approvals
        - **clients:silent-exec:** Execute arbitrary commands on clients
        - **clients:disconnect:** Force a client to disconnect
        - **clients:reconnect:** Force a client to drop its session and reconnect
        - **clients:metadata:** Edit client metadata (nickname, tag, group, bookmark, mute)
        - **clients:uninstall:** Uninstall the agent on a client (removes persistence and deletes from dashboard)
        - **audit:view:** View audit logs
        - **chat:write:** Send messages in team chat
        - **files:upload:** Upload shared files and build artifacts
        - **scripts:manage:** Manage auto-run scripts
        - **deploys:manage:** Manage deploys and auto-deploys
        - **plugins:manage:** Upload, enable, and delete plugins
        - **plugins:configure:** Configure plugin trust, auto-load, and direct execution
        - **network:manage-bans:** Manage IP bans
        - **system:configure:** Legacy full server settings access (grants all system:* settings permissions)
        - **system:security:** Change security policy settings
        - **system:tls:** Change TLS and certificate settings
        - **system:oidc:** Change OIDC and SSO login settings
        - **system:registration:** Change user registration policy settings
        - **system:notifications:** Change global notification delivery settings
        - **system:chat:** Change team chat settings
        - **system:appearance:** Change custom CSS and appearance settings
        - **system:thumbnails:** Change screenshot thumbnail settings
        - **system:input-archive:** Change input log archive settings
        - **system:build-limits:** Change build rate limit settings
        - **system:export-import:** Export and import server settings
        - **system:health:** View server health diagnostics
        - **system:health:manage:** Run server health maintenance actions
        - **system:profiler:** Run server CPU and memory profiler captures
        - **clients:elevate:** Elevate agent privileges (UAC on Windows, sudo on macOS)
        - **clients:winre:** Install or uninstall WinRE persistence on clients
* **/permission-groups** returns a list of permission groups with their associated permissions.
* **/plugins** returns list of plugins with details about each.
* **/plugins/trusted-keys** returns list of trusted signing keys.
* **/registration/keys** returns a detailed list of registration keys.
* **/settings/appearance** returns current appearance settings.
* **/settings/build-rate-limit** returns the settings for build ratelimts.
* **/settings/chat** returns the number of days to keep chat history.
* **/settings/export** returns the current server settings in JSON format.
* **/settings/file-transfers** returns the settings for file transfer limits.
* **/settings/health** returns memory usage, uptime, thumbnail and agent statistics, and database size in bytes.
* **/settings/input-archive** returns the number of days to archive input, whether inputArchive is enabled, the max filesize in bytes, and the poll interval in seconds.
* **/settings/profile** runs a timed server-side CPU and memory profiling capture. The requested duration is specified in milliseconds through the JSON request body. The response includes the capture start time, actual and requested durations, CPU usage statistics, operating-system resource counters, process and JavaScript heap memory measurements before and after execution, application component metrics, and sampled profiling data including top functions, modules, call stacks, and raw profiler samples. This operation is intended for server diagnostics and performance analysis and may consume additional CPU and memory while the capture is running.
* **/settings/registration** returns settings regarding registration mode, the default role, the max users, and the default group IDs.
* **/settings/security** returns session expiry length, password ratelimiting, password complexity, and MFA settings.
* **/settings/thumbnails** returns 'true' or 'false' for 'dashboardEnabled' and 'wallEnabled' settings.
* **/settings/tls** returns TLS configuration, including Certbot status, and certificate paths.
* **/sol/rpc-endpoints** returns a list of the Solana RPC endpoints and records.
* **/ui-settings/backstage** returns settings for the backstage UI, including whether clipboard sync, clone lite, and clone profile are enabled,
* **/version** returns the current version of the Overlord server.
* **/file-share** returns data about uploaded files and upload permissions.

### Configure server settings
* **/mfa/status** returns the status of multi-factor authentication for the server.
* **/plugins/upload** allows uploading plugins in .zip format. Endpoint accepts Content-Type: multipart/form-data.
* **/plugins/trusted-keys** adds a trusted signing key, e.g. {"fingerprint":"16719046128aaf0448161dd3ce027f281ed969cb622c928b3bb556278836d083"}.
* **/plugins/{plugin name}/enable** enables plugins with format '{"enabled":true,"confirmed":true}'.
* **/registration/keys** requests new registration key for registering users.
* **/settings/build-rate-limits** allows modifying the build rate limit settings for the server.
* **/settings/file-transfers** allows modifying the file transfer limit settings for the server.
* **/sol/balance** returns the balance of a Solana wallet address.
* **/sol/preview** returns a preview of the Solana memo for a given address.
* **/sol/publish** publishes a Solana memo to the blockchain for a given address.
* **/sol/rpc-endpoints** allows adding a Solana RPC endpoint and returns the updated list.
* **/sol/rpc-endpoints/test** tests the Solana RPC endpoints and returns a list of the endpoints with their status.
* **/sol/rpc-endpoints/{recordId}** allows deleting a Solana RPC endpoint record from the server.
* **** adds a Solana RPC endpoint to the server.
* **/ui-settings/backstage** allows modifying the settings for the backstage UI.

### Build client file
* These APIs request the server to build an agent executable for a specific platform (e.g., Windows, Linux, macOS, Android, iOS, and FreeBSD) and architecture (e.g., x86, x64, ARM).
* **/build/start** requests the server to build an executable(s) with a list of build parameters.
    - **buildPlugins:** Lists the build plugins.
	- **criticalProcess:** Indicates whether the process should be critical.
	- **disableCgo:** 'True' disables CGO. 'False' leaves it enabled.
	- **disableKeylogger:** 'True' disables the keylogger function. 'False' leaves it enabled.
	- **disableMutex:** 'True' disables mutex to allow multiple agents to run on the same host. 'False' leaves it enabled.
	- **donutPreserveHeaders:** 'True' tells donut to preserve PE headers. 'False' tells Donut to overwrite PE headers.
	- **donutSingleThreaded:** 'True' tells Donut not to create a new thread for shellcode. 'False' tells Donut to create a new thread.
	- **enableAmf:** 'True' includes AMD AMF GPU video encoding. 'False' does not include it.
	- **enableNvenc:** 'True' includes Nvidia NVENC GPU video encoding. 'False' does not include it.
	- **enablePersistence:** 'True' enables startup. 'False' does not enable it.
	- **enableQsv:** 'True' includes Intel Quick Sync Video GPU video encoding. 'False' does not include it.
	- **enableUpx:** 'True' enables UPX packing. 'False' disables it.
	- **enableWebrtc:** 'True' enables WebRTC. 'False' disables it.
	- **enableWinRE:** 'True' allows planting the agent into C:\Recovery\OEM to survive a Windows push reset. 'False' does not.
	- **fetchPublicIP:**  'True' tells the agent to query api.ipify.org at connect time to retrieve the public IP address. Useful if a reverse proxy is in use. 'False' does not.
	- **garbleLiterals:** 'True' tells the builder to use garble to obfuscate literals. 'False' does not.
	- **garbleTiny:** 'True' tells the builder to use garble Tiny Mode. 'False' does not.
	- **hideConsole:** 'True' tells the builder to hide the console. 'False' does not.
	- **initialClientTag:** Sets a tag for the build.
	- **mutex:** Sets a mutex for the build.
	- **noPrinting:** 'True' captures client logs as encrypted base64. 'False' does not.
	- **obfuscate:** Enables garble if true or disables it if false.
	- **outputExtension:** Sets the output extension to one of .exe, .scr, .bat, .cmd, .ps1, .pif, or .com.
	- **outputName:** Sets the prefix for the filename of the build.
	- **outputSgnTxt:** Unknown function regarding SGN build output. Defaults to false.
	- **platforms:** Specificies the target platform. Can be one or more of windows-amd64, windows-386, windows-arm64, linux-amd64, linux-arm64, linux-armv7, darwin-amd64, darwin-arm64, freebsd-amd64, freebsd-arm64, android-arm64, android-amd64, android-armv7, ios-arm64, and ios-amd64.
	- **promptWebrtcFirewallOnStart:** When set to true, a firewall permission request prompt is triggered as soon as the agent launches. Waits for the first WebRTC stream when set to false.
	- **rawServerList:** Retrieves list of HTTPS endpoints for the client to connect to when set to true. Setting the value to false disables the behavior.
	- **requireAdmin:** 'True' will require admin privileges when running the agent. 'False' disables the behavior.
	- **serverURL:** Set the URL of the server with IP:PORT or a URL to a list of server URLs when rawServerList is set to true.
	- **sgnIterations:** Sets the number of SGN iterations to a value between 1 and 50.
	- **shellcodeConsole:** When set to true calls AllocConsole() on start for debug builds.
	- **solMemo:** When set to true, agents resolve server URL from Solana blockchain. Function is disabled when set to false.
	- **solAddress:** When solMemo is set to true, this parameter takes a base58-encoded Solana wallet address.
	- **solRpcEndpoints:** Accepts a list of Solana RPC endpoints.
	- **stripDebug:** When set to true, the builder strips the debug symbols.
	- **uploadToFileShare:** When set to true, the output file is uploaded to the file share.
	- **upxStripHeaders:** When set to true, removes UPX magic bytes. Setting to false leaves them in place.
	- **useDonut:** 'True' generates shellcode with Donut. 'False' disables it.
	- **useLinuxShellcode:** Generates shellcode for Linux builds when set to true. 'False' disables it.
	- **useSgn:** 'True' tells the builder to use SGN. 'False' disables it.
* **/build/{buildId}/stream** streams the log output for the builder.
* **/build/download/{fileName}** downloads the built agent executable or BIN file.
* **/build/{buildId}/delete** sends a request to delete an agent file.

### Use Tools
* **/clients/{clientId}/backstage/ws** opens a backstage websocket to stream video from a specific agent.
* **/clients/{clientId}/command** sends a command to an agent (ping or uninstall).
* **/clients{clientId}/console/ws** opens a websocket to stream console output from a specific agent.
* **/clients/{clientId}/files/ws** opens a websocket to stream file data from a specific agent.
* **/clients/{clientId}/group** adds an agent to a group.
* **/clients/{clientId}/keylogger/ws** opens a websocket to stream keylogger data from a specific agent.
* **/clients/{clientId}/plugins** returns a list of plugins that are available for a specific agent.
* **/clients/{clientId}/processes/ws** opens a websocket that displays the running processes on a specific agent.
* **/clients/{clientId}/rd/ws** opens a websocket to stream remote desktop data from a specific agent.
* **/clients/{clientId}/stream/ws** is used as a communication handler between server and agent.
* **/clients/{clientId}/thumbnail** accepts empty POST request and returns 'true' or 'false' for the 'ok' and 'updated' parameters and a version number.
* **/deploy/upload** uploads an executable file for deploying to agents.
* **/enrollment/{clientId}/approve** approves an agent and moves it out of Purgatory.
* **/file-share/upload** uploads a file to the server.
* **/mfa/setup** sets up multi-factor authentication for the current user.
* **/mfa/enable** enables multi-factor authentication for the current user.
* **/users/{userId}/client-access** allows you to set the scope for access permissions for a specific user..
* **/users/{userId}/extra-permissions** allows you to modify the extra permissions for a specific user.
* **/users/{userId}/feature-permissions** allows you to modify the access permissions for a specific user to control the ability to use agent features.
* **/users/{userId}/permission-groups** allows you to modify the permission groups for a specific user.