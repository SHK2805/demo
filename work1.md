Key Findings from Testing:

Rogue CA was installed only in the personal profile.
Work profile certificate installation was not possible.
Microsoft Authenticator was installed in the personal profile.
JWT token observed during Graph communication.
Passkey registration failed due to policy restriction.
Captured token had limited scopes:
email
openid
profile
UserAuthenticationMethod.Read
UserAuthenticationMethod.ReadWrite
Token allowed limited Microsoft Graph enumeration.
No sensitive corporate data accessed.
No MFA manipulation observed.
No certificate pinning bypass attempted.
Device was non-rooted.
