"""
CrewGraph-AI v3.0 - Universal Web Interface
Complete web app to create, manage and run unlimited AI agents for any task
Social Media, Freelance, Business, Development, Research, Personal - Everything Automated!
"""

import gradio as gr
import asyncio
from universal_agents import CrewGraphUniversal, Config
import json
from datetime import datetime
import os

# Initialize system
system = CrewGraphUniversal()

# ==================== UI FUNCTIONS ====================

def get_agent_categories():
    """Get all available agent categories"""
    categories = system.factory.get_available_categories()
    result = "## 📋 Available Agent Categories\n\n"
    
    for category, roles in categories.items():
        result += f"### {category.replace('_', ' ').title()}\n"
        for role in roles:
            result += f"- {role}\n"
        result += "\n"
    
    return result

def create_custom_agent_ui(name, category, role, goal, backstory, skills_text):
    """Create a custom agent from UI inputs"""
    try:
        skills = [s.strip() for s in skills_text.split('\n') if s.strip()]
        
        agent = system.create_custom_agent(
            name=name,
            category=category,
            role=role,
            goal=goal,
            backstory=backstory,
            skills=skills
        )
        
        return f"✅ **Agent '{name}' created successfully!**\n\nCategory: {category}\nRole: {role}\nSkills: {len(skills)}\n\nYou can now use this agent to run autonomous tasks."
    except Exception as e:
        return f"❌ Error creating agent: {str(e)}"

def run_autonomous_task_ui(agent_name, task):
    """Run an autonomous task with selected agent"""
    try:
        if agent_name not in [a['name'] for a in system.factory.list_agents()]:
            return f"❌ Agent '{agent_name}' not found. Please create or select an agent first."
        
        result = system.run_autonomous_task(agent_name, task)
        
        return f"## ✅ Task Completed!\n\n**Agent:** {agent_name}\n**Task:** {task}\n\n---\n\n{result}"
    except Exception as e:
        return f"❌ Error running task: {str(e)}"

def list_agents_ui():
    """List all created agents"""
    agents = system.factory.list_agents()
    
    if not agents:
        return "No agents created yet. Create your first agent above!"
    
    result = "## 🤖 Your Active Agents\n\n"
    for agent in agents:
        result += f"### {agent['name']}\n"
        result += f"- **Category:** {agent['category']}\n"
        result += f"- **Role:** {agent['role']}\n"
        result += f"- **Goal:** {agent['goal'][:100]}...\n"
        result += f"- **Skills:** {len(agent['skills'])}\n"
        result += f"- **Created:** {agent['created_at']}\n\n"
    
    return result

def quick_start_agent(use_case):
    """Quick start with pre-built agent templates"""
    try:
        agent = system.quick_start(use_case)
        return f"✅ **Pre-built {use_case.replace('_', ' ')} agent created!**\n\nName: {agent.role}\nReady to use immediately."
    except Exception as e:
        return f"❌ Error: {str(e)}"

def delete_agent_ui(agent_name):
    """Delete an agent"""
    success = system.factory.delete_agent(agent_name)
    if success:
        return f"✅ Agent '{agent_name}' deleted successfully!"
    else:
        return f"❌ Agent '{agent_name}' not found."

# ==================== WEB INTERFACE ====================

with gr.Blocks(title="CrewGraph-AI v3.0 | Universal Agent Factory", theme=gr.themes.Soft()) as demo:
    
    gr.Markdown("""
    # 🚀 CrewGraph-AI v3.0 - Universal Agent Factory
    
    ### Create Unlimited AI Agents for ANY Task - Fully Autonomous!
    
    **Categories:** Social Media | Freelance (Fiverr/Upwork) | Business | Development | Content | Research | Personal | Automation
    
    🔹 Create custom agents with specific skills  \n    🔹 Use pre-built templates for common tasks  \n    🔹 Run autonomous workflows  \n    🔹 100% Local & Free - No API Costs
    """)
    
    with gr.Tabs():
        
        # Tab 1: Quick Start
        with gr.TabItem("⚡ Quick Start"):
            gr.Markdown("### Pre-built Agent Templates - Ready in 1 Click!")
            
            with gr.Row():
                with gr.Column():
                    use_case_dropdown = gr.Dropdown(
                        choices=[
                            ("📱 Social Media Manager", "social_media"),
                            ("💼 Fiverr Ranking Specialist", "fiverr"),
                            ("🏢 Business Automator", "business"),
                            ("💻 Full Stack Developer", "development")
                        ],
                        label="Select Use Case"
                    )
                    quick_start_btn = gr.Button("🚀 Create Agent", variant="primary")
                    quick_start_output = gr.Textbox(label="Result", lines=5)
                    
                    quick_start_btn.click(
                        fn=quick_start_agent,
                        inputs=[use_case_dropdown],
                        outputs=[quick_start_output]
                    )
            
            gr.Markdown("""
            **What these agents can do:**
            - **Social Media Manager:** Auto-post content, engage followers, analyze trends, manage multiple platforms
            - **Fiverr Optimizer:** Optimize gigs, write proposals, boost rankings, manage reviews
            - **Business Automator:** Handle operations, automate workflows, manage CRM, generate reports
            - **Full Stack Dev:** Build apps, debug code, deploy to cloud, maintain systems
            """)
        
        # Tab 2: Custom Agent Creator
        with gr.TabItem("🛠️ Create Custom Agent"):
            gr.Markdown("### Build Your Own Specialized AI Agent")
            
            with gr.Row():
                with gr.Column(scale=1):
                    agent_name = gr.Textbox(label="Agent Name", placeholder="e.g., InstagramGuru, FiverrPro, EcomBoss")
                    agent_category = gr.Dropdown(
                        choices=list(Config.AGENT_CATEGORIES.keys()),
                        label="Category"
                    )
                    agent_role = gr.Textbox(label="Role", placeholder="e.g., Instagram Growth Expert, Fiverr SEO Specialist")
                    agent_goal = gr.Textbox(
                        label="Goal",
                        placeholder="What should this agent achieve?",
                        lines=3
                    )
                    agent_backstory = gr.Textbox(
                        label="Background/Expertise",
                        placeholder="Describe the agent's experience and expertise",
                        lines=4
                    )
                    agent_skills = gr.Textbox(
                        label="Skills (one per line)",
                        placeholder="List all skills this agent should have",
                        lines=6
                    )
                    create_agent_btn = gr.Button("✨ Create Agent", variant="primary")
                
                with gr.Column(scale=1):
                    create_agent_output = gr.Textbox(label="Creation Result", lines=15)
            
            create_agent_btn.click(
                fn=create_custom_agent_ui,
                inputs=[agent_name, agent_category, agent_role, agent_goal, agent_backstory, agent_skills],
                outputs=[create_agent_output]
            )
        
        # Tab 3: Run Autonomous Tasks
        with gr.TabItem("⚙️ Run Tasks"):
            gr.Markdown("### Execute Autonomous Tasks with Your Agents")
            
            with gr.Row():
                with gr.Column():
                    # Dynamic agent selector
                    def get_agent_names():
                        agents = system.factory.list_agents()
                        return [a['name'] for a in agents] if agents else ["No agents created"]
                    
                    agent_selector = gr.Dropdown(
                        choices=get_agent_names(),
                        label="Select Agent",
                        interactive=True
                    )
                    
                    refresh_agents_btn = gr.Button("🔄 Refresh Agent List")
                    
                    task_input = gr.Textbox(
                        label="Task Description",
                        placeholder="Describe what you want the agent to do...",
                        lines=4
                    )
                    
                    run_task_btn = gr.Button("🚀 Run Autonomous Task", variant="primary")
                    task_output = gr.Textbox(label="Result", lines=15)
                    
                    refresh_agents_btn.click(
                        fn=lambda: gr.Dropdown(choices=get_agent_names()),
                        outputs=[agent_selector]
                    )
                    
                    run_task_btn.click(
                        fn=run_autonomous_task_ui,
                        inputs=[agent_selector, task_input],
                        outputs=[task_output]
                    )
            
            gr.Markdown("""
            **Example Tasks:**
            - "Create a 30-day Instagram content calendar for my fitness brand"
            - "Optimize my Fiverr gig 'Logo Design' to rank #1"
            - "Analyze competitors and suggest pricing strategy"
            - "Build a complete e-commerce website with payment integration"
            - "Research trending topics in AI and write a blog post"
            """)
        
        # Tab 4: Manage Agents
        with gr.TabItem("📊 Manage Agents"):
            gr.Markdown("### View and Manage All Your Agents")
            
            with gr.Row():
                with gr.Column():
                    list_agents_btn = gr.Button("📋 Refresh Agent List", variant="secondary")
                    agents_list_output = gr.Textbox(label="Active Agents", lines=20)
                    
                    list_agents_btn.click(
                        fn=list_agents_ui,
                        outputs=[agents_list_output]
                    )
                
                with gr.Column():
                    gr.Markdown("### Delete Agent")
                    delete_agent_name = gr.Dropdown(
                        choices=[],
                        label="Select Agent to Delete"
                    )
                    delete_btn = gr.Button("🗑️ Delete Agent", variant="stop")
                    delete_output = gr.Textbox(label="Result")
                    
                    def update_delete_dropdown():
                        agents = system.factory.list_agents()
                        names = [a['name'] for a in agents]
                        return gr.Dropdown(choices=names if names else ["No agents"])
                    
                    delete_btn.click(
                        fn=delete_agent_ui,
                        inputs=[delete_agent_name],
                        outputs=[delete_output]
                    )
        
        # Tab 5: Categories Reference
        with gr.TabItem("📚 Agent Categories"):
            categories_output = gr.Markdown()
            
            def load_categories():
                return get_agent_categories()
            
            demo.load(fn=load_categories, outputs=[categories_output])
        
        # Tab 6: Examples & Tutorials
        with gr.TabItem("📖 Examples"):
            gr.Markdown("""
            ## 💡 Real-World Use Cases
            
            ### 📱 Social Media Management
            ```
            Agent: SocialMediaPro
            Tasks:
            - Create daily posts for Instagram, Twitter, LinkedIn
            - Analyze engagement metrics and optimize strategy
            - Respond to comments and DMs automatically
            - Schedule posts at optimal times
            - Track trending hashtags and topics
            ```
            
            ### 💼 Fiverr/Upwork Success
            ```
            Agent: FiverrRankBooster
            Tasks:
            - Optimize gig titles, tags, and descriptions for SEO
            - Write custom proposals that convert
            - Analyze competitor pricing and adjust yours
            - Manage client reviews and ratings
            - Track ranking improvements daily
            ```
            
            ### 🏢 Business Automation
            ```
            Agent: BizAutoPilot
            Tasks:
            - Automate email marketing campaigns
            - Manage CRM and follow up with leads
            - Generate weekly business reports
            - Optimize operational workflows
            - Handle customer support tickets
            ```
            
            ### 💻 Software Development
            ```
            Agent: CodeMaster3000
            Tasks:
            - Build complete web applications from scratch
            - Debug and fix errors autonomously
            - Write unit tests and documentation
            - Deploy to AWS/GCP/Azure
            - Monitor and maintain production systems
            ```
            
            ### 🔬 Research & Analysis
            ```
            Agent: ResearchPro
            Tasks:
            - Conduct deep web research on any topic
            - Analyze market trends and competitors
            - Write comprehensive reports with citations
            - Extract insights from large datasets
            - Stay updated with latest industry news
            ```
            
            ---
            
            ## 🎯 How to Get Started
            
            1. **Quick Start:** Use pre-built templates for common tasks
            2. **Custom Agent:** Create specialized agents for your unique needs
            3. **Run Tasks:** Give clear instructions and let agents work autonomously
            4. **Scale:** Create multiple agents for different aspects of your business
            
            **Pro Tip:** Combine multiple agents in workflows for complex projects!
            """)
    
    gr.Markdown("""
    ---
    ### 🌟 CrewGraph-AI v3.0 - The Ultimate AI Automation Platform
    
    **Features:** Unlimited Agents | Any Category | Full Autonomy | 100% Local | Zero API Costs
    
    Made with ❤️ for entrepreneurs, freelancers, and businesses who want to automate everything!
    """)

# Launch the app
if __name__ == "__main__":
    print("🚀 Launching CrewGraph-AI v3.0 Web Interface...")
    print("📍 Open http://localhost:7860 in your browser")
    demo.launch(server_name="0.0.0.0", server_port=7860)
