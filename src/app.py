import streamlit as st
from password_analyzer import calculate_entropy, check_pwned_password
from phishing_detector import PhishingDetector

st.set_page_config(
    page_title="Cybersecurity AI Toolkit", page_icon="🛡️", layout="wide"
)

st.title("🛡️ Cybersecurity AI Toolkit")
st.markdown(
    "Plateforme centralisée d'analyse de sécurité : Mots de passe & Détection"
    " de Phishing par IA."
)

tab1, tab2 = st.tabs(
    ["🔒 Password Security Analyzer", "📧 Phishing Email Detector"]
)

# --- TAB 1 : Passwords ---
with tab1:
  st.header("Analyseur de Robustesse de Mot de Passe")
  pwd_input = st.text_input("Entrez un mot de passe à tester :", type="password")

  if pwd_input:
    entropy = calculate_entropy(pwd_input)
    pwned_count = check_pwned_password(pwd_input)

    col1, col2 = st.columns(2)
    with col1:
      st.metric(label="Entropie (bits)", value=f"{entropy} bits")
      if entropy < 50:
        st.warning("⚠️ Mot de passe faible.")
      else:
        st.success("✅ Mot de passe robuste.")

    with col2:
      if pwned_count > 0:
        st.error(
            f"🚨 COMPROMIS ! Ce mot de passe apparaît {pwned_count} fois dans"
            " des fuites de données."
        )
      elif pwned_count == 0:
        st.success(
            "🟢 Aucune fuite détectée dans les bases publiques (HIBP)."
        )
      else:
        st.info("Impossible de contacter l'API Have I Been Pwned.")

# --- TAB 2 : Phishing ---
with tab2:
  st.header("Détecteur d'E-mail de Phishing (Machine Learning)")
  email_text = st.text_area("Collez le contenu de l'e-mail suspect ici :")

  if st.button("Analyser l'e-mail"):
    if email_text.strip():
      detector = PhishingDetector()
      result = detector.predict_email(email_text)

      if result["is_phishing"]:
        st.error(
            f"🚨 ALERTE PHISHING DÉTECTÉ ! (Confiance :"
            f" {result['confidence']}%)"
        )
      else:
        st.success(
            f"🟢 E-mail considéré comme sûr (Confiance :"
            f" {result['confidence']}%)"
        )

      if result["extracted_urls"]:
        st.markdown("### Liens détectés dans le message :")
        for u in result["extracted_urls"]:
          st.code(u)
    else:
      st.warning("Veuillez entrer du texte à analyser.")