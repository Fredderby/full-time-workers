import streamlit as st
import re
from datetime import datetime
from zones import zones_data  # imported zone from a dictionary
from connect import cred  # imported a connection to the google sheet


class FullTimeWorkersForm:
    """Professional form for Full-Time Workers Registration - REGISTRATION CLOSED"""

    def __init__(self):
        self.form_data = {}
        self.session_state = st.session_state
        self.client = cred()
        self.spreadsheet = self.client.open("mini_congress")
        self.worksheet = self.spreadsheet.worksheet("fulltimeworkers")

        # Initialize session state for form persistence
        if 'submitted' not in self.session_state:
            self.session_state.submitted = False
        if 'form_values' not in self.session_state:
            self.session_state.form_values = {}

    def display_closed_message(self):
        """Display registration closed message"""
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 10px; border: 2px solid #ff6b6b;">
            <h1 style="color: #ff6b6b; font-size: 48px;">⛔</h1>
            <h2 style="color: #d32f2f;">REGISTRATION CLOSED</h2>
            <h3 style="color: #555;">Full-Time Workers Registration Has Ended</h3>
            <hr style="border-color: #ff6b6b;">
            <p style="font-size: 16px; color: #666;">
                The registration period for Full-Time Workers has officially ended.<br>
                No new submissions are being accepted at this time.
            </p>
            <p style="font-size: 14px; color: #888; margin-top: 20px;">
                <i>For inquiries, please contact the Data Analyst.</i>
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Additional information box
        with st.container(border=True):
            st.markdown("### ℹ️ **Important Information**")
            st.markdown("""
            - Registration closed on: **12.30pm today Sunday 18/01/2026**
            - No further applications will be processed
            - For status inquiries, contact: **Data Analyst**
            """)

    def validate_contact(self, contact):
        """Validate contact number - exactly 10 digits, no symbols"""
        if not contact:
            return False, "Contact number is required"

        # Remove any whitespace
        contact = contact.strip()

        # Check if it's exactly 10 digits and contains only numbers
        if not contact.isdigit():
            return False, "Contact must contain only digits (0-9)"

        if len(contact) != 10:
            return False, "Contact must be exactly 10 digits"

        return True, contact

    def format_name(self, name):
        """Format name to proper case"""
        if not name:
            return name
        # Split by spaces, capitalize each word, and join back
        return ' '.join(word.capitalize() for word in name.strip().split())

    def format_position(self, position):
        """Format position to proper case"""
        if not position:
            return position
        return ' '.join(word.capitalize() for word in position.strip().split())

    def display_section_a(self):
        """Display Section A - Worker Information (DISABLED)"""
        with st.container(border=True):
            st.markdown("### 📍 REGISTRATION FORM")
            st.markdown('<p style="color: #ff6b6b; font-weight: bold;">🚫 FORM DISABLED - REGISTRATION CLOSED</p>', 
                       unsafe_allow_html=True)
            st.markdown("---")

            # All form fields disabled
            col1, col2 = st.columns(2)

            with col1:
                zones = st.selectbox(
                    "🏛️ **Zone:**",
                    list(zones_data.keys()),
                    index=None,
                    placeholder="Select zone...",
                    key="zone_select",
                    disabled=True  # Disabled
                )
                self.form_data['zone'] = zones

            with col2:
                if zones:
                    regions_in_zone = list(zones_data[zones].keys())
                    selected_region = st.selectbox(
                        "📍 **Region:**",
                        regions_in_zone,
                        index=None,
                        placeholder="Select region...",
                        key="region_select",
                        disabled=True  # Disabled
                    )
                    self.form_data['region'] = selected_region
                else:
                    st.selectbox(
                        "📍 **Region:**",
                        ["Please select zone first"],
                        disabled=True,
                        key="region_disabled"
                    )

            # 3. DIVISION Selection (disabled)
            if zones and selected_region:
                divisions_in_region = zones_data[zones][selected_region]
                selected_division = st.selectbox(
                    "🏢 **Division:**",
                    divisions_in_region,
                    index=None,
                    placeholder="Select division...",
                    key="division_select",
                    disabled=True  # Disabled
                )
                self.form_data['division'] = selected_division

            # 4. Name (disabled)
            name = st.text_input(
                "👤 **Full Name:**",
                placeholder="Enter full name (e.g., John Smith)",
                key="name_input",
                disabled=True  # Disabled
            )
            if name:
                self.form_data['name'] = self.format_name(name)

            # 5. Gender (disabled)
            col3, col4 = st.columns(2)

            with col3:
                gender = st.selectbox(
                    "⚥ **Gender:**",
                    ["", "Male", "Female"],
                    index=0,
                    placeholder="Select gender...",
                    key="gender_select",
                    disabled=True  # Disabled
                )
                self.form_data['gender'] = gender

            # 6. Position (disabled)
            with col4:
                position = st.text_input(
                    "💼 **Position/Title:**",
                    placeholder="Enter position (e.g., Field Officer)",
                    key="position_input",
                    disabled=True  # Disabled
                )
                if position:
                    self.form_data['position'] = self.format_position(position)

            # 7. Contact (disabled)
            contact = st.text_input(
                "📱 **Contact Number:**",
                placeholder="Enter 10-digit number (e.g., 0241234567)",
                max_chars=10,
                key="contact_input",
                disabled=True  # Disabled
            )
            if contact:
                is_valid, message = self.validate_contact(contact)
                if not is_valid:
                    st.error(f"❌ {message}")
                else:
                    self.form_data['contact'] = message

    def display_submission_section(self):
        """Display disabled submission button"""
        with st.container(border=True):
            submit_button = st.button(
                "🚫 **REGISTRATION CLOSED**",
                type="secondary",
                use_container_width=True,
                disabled=True  # Button disabled
            )

            st.info("⚠️ **Registration is no longer accepting new submissions.**")

    def validate_and_submit(self):
        """Registration closed - no submissions accepted"""
        st.error("❌ **Registration is closed. No new submissions are being accepted.**")
        return False

    def submit_to_google_sheets(self):
        """Registration closed - no data submission"""
        st.error("❌ **Cannot submit: Registration period has ended.**")
        return False

    def reset_form(self):
        """Reset form fields"""
        keys_to_reset = [
            'zone_select', 'region_select', 'division_select',
            'name_input', 'gender_select', 'position_input', 'contact_input'
        ]

        for key in keys_to_reset:
            if key in st.session_state:
                del st.session_state[key]

        self.form_data = {}

    def run(self):
        """Main method to run the form - Registration Closed"""
        # Display closure message
        self.display_closed_message()
        
        st.markdown("---")
        
        # Optionally show the disabled form for reference
        with st.expander("View Registration Form (Disabled)", expanded=False):
            self.display_section_a()
            self.display_submission_section()


def reg():
    """Main function to run the Full-Time Workers Registration form - REGISTRATION CLOSED"""
    form = FullTimeWorkersForm()
    form.run()


# Run the application
if __name__ == "__main__":
    # Set page configuration
    st.set_page_config(
        page_title="Registration Closed - Full-Time Workers",
        page_icon="⛔",
        layout="centered"
    )
    
    # Main title with closed status
    st.title("⛔ Full-Time Workers Registration - CLOSED")
    
    # Run the registration (closed) form
    reg()