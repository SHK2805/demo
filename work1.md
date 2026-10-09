Subject: Options for supporting multiple gateways/regions in the mobile banking app

Hi all,

We need the app to support multiple gateways/regions, so a user can switch regions without losing their existing registration. Today the library holds a single registration (keys on device and server) tied to one gateway. Below are the three options we have looked at.

OPTION 1: Per-gateway registrations in the library (full refactor)

How it works:
- Registration becomes a namespaced object keyed by gateway ID. Keys, server certificate/public key, device ID, tokens and push token are all stored per gateway.
- Each gateway gets its own key pair (Android Keystore aliases and iOS Keychain/Secure Enclave tags prefixed with the gateway ID).
- The library moves from a single global instance to a per-gateway client. Switching means changing which client the app uses; nothing is wiped.
- The existing registration is migrated into a default gateway entry so current users do not re-register.

Pros:
- Regions are fully independent. A compromise or revocation in one does not affect the others.
- Best fit for data-residency and regulatory requirements.
- No new central component, and each gateway needs no knowledge of the others.

Cons:
- Largest change. It touches the shared library, which is used by other apps, so it needs regression testing across all of them.
- Needs a careful, crash-safe migration for existing users.
- More key management and lifecycle handling (per-gateway unregister, push tokens, biometric invalidation, iOS reinstall, Android backup exclusion).

OPTION 2: Authentication/front server in front of the gateways (no library change)

How it works:
- The library registers once with the front server, which looks like "the gateway" to it. The front server maps each user/device to a region and routes to the regional gateways behind it.
- Switching regions is a server-side binding change, triggered by an app-level API call outside the library. Only one registration ever exists on the device.

Pros:
- No library change, so no impact on the other apps.
- Nothing on the device is wiped or migrated.

Cons:
- If the front server terminates the secure channel, it holds the device keys and effectively becomes a new global gateway, with the regional gateways turned into internal services. This is a highly sensitive component in a banking context (HSM-backed keys, strict auditing).
- If it is only a pass-through router, it cannot see inside the traffic and needs a routing hint from the client (header, path or hostname), which may itself need a library change.
- Routing all traffic and key material through one front door may defeat data-residency requirements.
- It becomes a global single point of failure and adds a network hop, so it must itself be multi-region.
- Regional gateways must trust the front server and receive device identity via signed assertions rather than directly.
- Switching semantics (re-authentication, in-flight sessions and tokens) must be defined server-side.

OPTION 3: Additive, opt-in namespace in the library (lighter change)

How it works:
- Add an optional namespace/gatewayId parameter to library initialisation. If it is not supplied, the library behaves exactly as today (same key aliases, same storage), so existing apps are unaffected.
- Only this app opts in, and the library then keeps a separate registration (and keys) per namespace, as in Option 1.
- The app holds one client per namespace and switches between them.

Pros:
- Backward compatible, so the risk to other apps is small.
- Keeps regions independent with no new central component.
- Much smaller than a full refactor, with no migration needed for apps that do not opt in.

Cons:
- Still a change to the shared library, so it needs release and regression testing.
- The library must support multiple concurrent instances without shared global state, which may be the hardest part depending on how it is built today.
- The app is responsible for the gateway list, switching UX and re-authentication policy.

Not recommended: snapshotting and restoring the library's stored registration on each switch. It looks like a no-change option, but it is fragile with hardware-backed Keystore/Keychain keys.

RECOMMENDATION
- If regions exist for residency or regulatory reasons: Option 3 (or Option 1 if we want the full cleanup), with no shared front door.
- If regions are about routing or UX and the library truly cannot change: Option 2, designed as a proper multi-region global gateway.

Two answers would settle the choice:
1. Why do the regions exist (residency/regulation, capacity, or separate entities/brands)?
2. Does the library let the app set the base URL or custom headers at runtime, and can it run more than one instance today?

Happy to walk through any of these in more detail.

Thanks,
[Name]
