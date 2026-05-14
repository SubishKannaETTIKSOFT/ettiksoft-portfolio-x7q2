/* ============================================================
   ETTIKSOFT Auth Guard
   Silently skips on localhost. On production, enforces
   Microsoft MSAL login restricted to @ettiksoft.com.
   ============================================================ */
(async function () {
  // Skip auth on localhost
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

  const msalInstance = new msal.PublicClientApplication({
    auth: {
      clientId: cfg.clientId,
      authority: cfg.authority,
      redirectUri: cfg.redirectUri
    },
    cache: {
      cacheLocation: "localStorage",
      storeAuthStateInCookie: false
    }
  });

  await msalInstance.initialize();

  // Handle redirect response (returning from login)
  // redirectUri must match exactly what was passed to loginRedirect
  const response = await msalInstance.handleRedirectPromise(cfg.redirectUri);

  const accounts = msalInstance.getAllAccounts();
  const activeAccount = response?.account || accounts[0];

  if (activeAccount) {
    const email = activeAccount.username;

    // Enforce @ettiksoft.com domain
    if (!email.endsWith(cfg.allowedDomain)) {
      await msalInstance.logoutRedirect({
        postLogoutRedirectUri: cfg.redirectUri
      });
      return;
    }

    // Store user info globally
    window.__ETTIKSOFT_USER__ = {
      name: activeAccount.name,
      email: email
    };

    // Show user name in topbar if badge exists
    const badge = document.getElementById("auth-user-badge");
    if (badge) {
      badge.textContent = activeAccount.name;
      badge.style.display = "inline-flex";
    }

    // Wire logout button if exists
    const logoutBtn = document.getElementById("auth-logout-btn");
    if (logoutBtn) {
      logoutBtn.addEventListener("click", async () => {
        await msalInstance.logoutRedirect({
          postLogoutRedirectUri: cfg.redirectUri
        });
      });
    }

    return; // Authenticated successfully
  }

  // No account found — redirect to Microsoft login
  // redirectUri passed explicitly here (MSAL requirement — msalConfig alone is not enough)
  console.log('REDIRECT URI BEING SENT:', cfg.redirectUri);
  console.log('MSAL CONFIG:', JSON.stringify({
    clientId: cfg.clientId,
    authority: cfg.authority,
    redirectUri: cfg.redirectUri
  }));
  await msalInstance.loginRedirect({
    scopes: ["User.Read"],
    prompt: "select_account",
    redirectUri: "https://subishkannaettiksoft.github.io/ettiksoft-portfolio-x7q2"
  });
})();
