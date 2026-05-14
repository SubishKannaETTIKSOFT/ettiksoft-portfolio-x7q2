/* ============================================================
   ETTIKSOFT Auth Guard
   Silently skips on localhost. On production, enforces
   Microsoft MSAL login restricted to @ettiksoft.com.
   ============================================================ */
(async function () {
  const isLocal =
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1";
  if (isLocal) return;

  // Load MSAL from local bundle (no CDN dependency)
  await new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = "./msal-browser.min.js";
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });

  const cfg = ETTIKSOFT_AUTH_CONFIG;

  const msalConfig = {
    auth: {
      clientId: cfg.clientId,
      authority: cfg.authority,
      redirectUri: "https://subishkannaettiksoft.github.io/ettiksoft-portfolio-x7q2"
    },
    cache: {
      cacheLocation: "sessionStorage",
      storeAuthStateInCookie: true
    }
  };

  const msalInstance = new msal.PublicClientApplication(msalConfig);
  await msalInstance.initialize();

  // CRITICAL: Always handle redirect first
  // This processes the auth code from Microsoft
  let tokenResponse = null;
  try {
    tokenResponse = await msalInstance.handleRedirectPromise();
  } catch (err) {
    console.error("Redirect error:", err);
    // Clear any bad state and try fresh login
    sessionStorage.clear();
    await msalInstance.loginRedirect({
      scopes: ["User.Read"],
      redirectUri: "https://subishkannaettiksoft.github.io/ettiksoft-portfolio-x7q2"
    });
    return;
  }

  // Check if we just completed a login
  const account = tokenResponse?.account ||
                  msalInstance.getAllAccounts()[0];

  if (account) {
    // Validate domain
    if (!account.username.endsWith("@ettiksoft.com")) {
      await msalInstance.logoutRedirect({
        postLogoutRedirectUri: "https://subishkannaettiksoft.github.io/ettiksoft-portfolio-x7q2"
      });
      return;
    }

    // Success - set active account and show user
    msalInstance.setActiveAccount(account);
    window.__ETTIKSOFT_USER__ = {
      name: account.name,
      email: account.username
    };

    const badge = document.getElementById("auth-user-badge");
    if (badge) {
      badge.textContent = account.name;
      badge.style.display = "inline-flex";
    }

    const logoutBtn = document.getElementById("auth-logout-btn");
    if (logoutBtn) {
      logoutBtn.addEventListener("click", async () => {
        msalInstance.setActiveAccount(account);
        await msalInstance.logoutRedirect({
          postLogoutRedirectUri: "https://subishkannaettiksoft.github.io/ettiksoft-portfolio-x7q2"
        });
      });
    }
    return; // Authenticated - let page load
  }

  // No account - go to login
  await msalInstance.loginRedirect({
    scopes: ["User.Read"],
    redirectUri: "https://subishkannaettiksoft.github.io/ettiksoft-portfolio-x7q2"
  });
})();
