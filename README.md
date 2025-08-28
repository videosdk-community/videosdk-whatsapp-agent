<div align="left">

# WhatsApp AI Voice Agent | VideoSDK

<div align="left" style="margin:0px 12px;">

This project is designed to be a streamlined alternative to complex setups, removing the need for middleware like n8n by connecting Twilio directly to the VideoSDK SIP Gateway using a TwiML Bin.

</div>
<div align="center">

![Architecture : Connecting Voice Agent to Telephony Agent](https://strapi.videosdk.live/uploads/whatsapp_ai_agent_adf0519bcc.png)

<div style="display:flex; width:100%; justify-content:center; gap:8px">
<a href="https://docs.videosdk.live/ai_agents/introduction" target="_blank"><img src="https://img.shields.io/badge/_Documentation-4285F4?style=for-the-badge" alt="Documentation"></a>
<a href="https://discord.gg/f2WsNDN9S5" target="_blank"><img src="https://img.shields.io/badge/_Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord Community"></a>
<a href="https://pypi.org/project/videosdk-agents/" target="_blank"><img src="https://img.shields.io/badge/_pip_install-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="PyPI Package"></a>
</div>

</div>

</div>

## Prerequisites

Before you begin, ensure you have the following:

- **Python 3.12+**
- **Docker** installed and running on your local machine.
- A **VideoSDK Account**. [Sign up here](https://videosdk.live/).
- A [**Twilio Account**](https://console.twilio.com) with a phone number that is approved for WhatsApp Business.
- A [**Google AI Studio API Key**](https://aistudio.google.com/app/apikey) for the Gemini model.

## Getting Started

Follow these steps to get your AI WhatsApp agent live.

### 1. Clone the Repository

```bash
git clone https://github.com/videosdk-community/videosdk-whatsapp-agent.git
cd videosdk-whatsapp-agent
```

### 2. Set Up Your Environment

Create a virtual environment and install the required Python packages.

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Create a Deployment ID & Configure Manifest

#### 3.a Create Deployment ID via API

This project includes a sample HTTP request file in the `http-req/` directory. You can use the popular VS Code extension **[REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)** to run this request directly from your editor.
Request File: `http-req/create-deployment-id.http`

```http
POST https://api.videosdk.live/ai/v1/ai-deployments
Authorization: VIDEOSDK_TOKEN
Content-Type: application/json

{
    "name": "AI Whatsapp Agent",
    "description":"AI Telephony Agents - Inbound/Outbound Calls"
}
```

#### 3.b Configure the Deployment Manifest (`videosdk.yaml`)

Open the `videosdk.yaml` file. You only need to set your deployment.

```yaml
# videosdk.yaml
version: "1.0"
deployment:
  id: "your-unique-deployment-id-goes-here" # <-- CHANGE THIS
  entry:
    path: main.py
secrets:
  VIDEOSDK_AUTH_TOKEN: "specify-your-videosdk-token"
```

_Note: After deployment `VIDEOSDK_TOKEN` & `VIDEOSDK_ROOM_ID` are loaded from your environment, Room Id is generated dynamically and will be automatically added to `main.py`_

### 4. Deploy the AI Agent

Now, deploy your agent to the VideoSDK cloud with a single command:

```bash
videosdk deploy
```

Once the deployment is successful, the CLI will confirm the **Deployment ID**. This is the unique ID you set in the `videosdk.yaml` file. Keep it handy for the final step!

![Output of Deployed Voice Agent](https://www.videosdk.live/_next/image?url=https%3A%2F%2Fassets.videosdk.live%2Fstatic-assets%2Fghost%2F2025%2F08%2Fvideosdk-deploy-.png&w=3120&q=75)

### 5. Configure VideoSDK & Twilio

This is where we connect the public phone number to your deployed agent.

#### **Part A: VideoSDK Inbound Gateway**

1.  Go to your [**VideoSDK Dashboard**](https://app.videosdk.live/login).
2.  Navigate to **Telephony -> Inbound Gateways** and click **"Add Inbound Gateway"**.
3.  Give it a name (e.g., `WhatsApp Agent Gateway`).
4.  VideoSDK will generate a unique **SIP URI**. **Copy this URI**.

#### **Part B: Twilio TwiML Bin**

1.  Go to your **Twilio Console**.
2.  Navigate to **Develop -> TwiML Bins** and create a new bin.
3.  Give it a "Friendly Name" (e.g., `Forward to VideoSDK`).
4.  In the TwiML code section, paste the following XML, **replacing `YOUR_VIDEOSDK_SIP_URI`** with the URI you copied from the VideoSDK dashboard:

    ```xml
    <Response>
      <Dial>
        <Sip>YOUR_VIDEOSDK_SIP_URI</Sip>
      </Dial>
    </Response>
    ```

5.  Save the TwiML Bin.
6.  Navigate to **Phone Numbers -> Manage -> Active numbers** and select your WhatsApp-enabled number.
7.  Under the "A Call Comes In" section, select **TwiML Bin** and choose the bin you just created. Save the configuration.

#### **Part C: VideoSDK Routing Rule**

1.  Go back to your **VideoSDK Dashboard**.
2.  Navigate to **Telephony -> Routing Rules** and create a new rule.
3.  Configure the rule as follows:
    - **Direction:** `Inbound`
    - **Gateway:** Select the `WhatsApp Agent Gateway` you created.
    - **Room Type:** `Dynamic` (This is crucial for handling multiple calls).
    - **Agent Type:** `Cloud`
    - **Deployment ID:** Select the unique ID of the agent you deployed.
4.  Save the Routing Rule.

### 7. You're Live!

That's it! Your AI voice agent is now live. Make a voice call to your number from WhatsApp to see it in action.
