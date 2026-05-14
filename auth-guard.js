/* ============================================================
   ETTIKSOFT Auth Guard
   Silently skips on localhost. On production, enforces
   Microsoft MSAL login restricted to @ettiksoft.com.
   ============================================================ */
(async function () {
  function showError(msg) {
    const overlay = document.getElementById("auth-loading");
    if (overlay) {
      overlay.innerHTML =
        '<div style="text-align:center;padding:20px;max-width:400px;">' +
        '<h2 style="color:#B85450;margin-bottom:16px;font-family:system-ui,sans-serif;">Authentication failed</h2>' +
        '<p style="color:#1F2937;margin-bottom:20px;font-family:system-ui,sans-serif;">' + msg + '</p>' +
        '<button onclick="localStorage.clear();sessionStorage.clear();location.href=\'https://subishkannaettiksoft.github.io/ettiksoft-portfolio-x7q2/\';" ' +
        'style="background:#5E8A7B;color:white;border:none;padding:10px 20px;' +
        'border-radius:6px;cursor:pointer;font-family:system-ui,sans-serif;">Try Again</button></div>';
    }
  }

  try {
    // Load MSAL from local bundle (no CDN dependency)
    await new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.src = "./msal-browser.min.js";
      script.onload = resolve;
      script.onerror = () => reject(new Error("Could not load MSAL library"));
      document.head.appendChild(script);
    });

    const cfg = ETTIKSOFT_AUTH_CONFIG;

    const msalInstance = new msal.PublicClientApplication({
      auth: {
        clientId: cfg.clientId,
        authority: cfg.authority,
        redirectUri: cfg.redirectUri,
        postLogoutRedirectUri: cfg.redirectUri,
        navigateToLoginRequestUrl: false
      },
      cache: {
        cacheLocation: "localStorage",
        storeAuthStateInCookie: true
      }
    });

    await msalInstance.initialize();

    // Process redirect from Microsoft (if any)
    const tokenResponse = await msalInstance.handleRedirectPromise();

    // Get account from response or existing session
    const account = tokenResponse?.account ||
                    msalInstance.getAllAccounts()[0];

    if (account) {
      // Domain restriction
      if (!account.username.endsWith(cfg.allowedDomain)) {
        showError("Access restricted to @ettiksoft.com accounts only.");
        setTimeout(() => msalInstance.logoutRedirect(), 3000);
        return;
      }

      // Authenticated successfully
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
          await msalInstance.logoutRedirect();
        });
      }

      // Remove loading overlay — reveal the app
      const overlay = document.getElementById("auth-loading");
      if (overlay) overlay.remove();
      return;
    }

    // No account — start login flow
    await msalInstance.loginRedirect({
      scopes: ["User.Read"],
      prompt: "select_account"
    });

  } catch (err) {
    console.error("Auth error:", err);
    showError("Could not complete sign-in. " +
              (err.message || "Please try again."));
    // No automatic retry — prevents infinite loops
  }
})();
