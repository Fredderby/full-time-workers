import streamlit as st
import re
from datetime import datetime
from zones import zones_data #imported zone from a dictionary
from connect import cred #imported a connection to the google sheet


class FullTimeWorkersForm:
    """Professional form for Full-Time Workers Registration"""
    
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
        """Display Section A - Worker Information"""
        with st.container(border=True):
            st.markdown("### 📍 REGISTRATION FORM")
            st.markdown("---")
            
            # 1. ZONE Selection
            col1, col2 = st.columns(2)
            
            with col1:
                zones = st.selectbox(
                    "🏛️ **Zone:**",
                    list(zones_data.keys()),
                    index=None,
                    placeholder="Select zone...",
                    key="zone_select"
                )
                self.form_data['zone'] = zones
            
            # 2. REGION Selection (depends on zone)
            with col2:
                if zones:
                    regions_in_zone = list(zones_data[zones].keys())
                    selected_region = st.selectbox(
                        "📍 **Region:**",
                        regions_in_zone,
                        index=None,
                        placeholder="Select region...",
                        key="region_select"
                    )
                    self.form_data['region'] = selected_region
                else:
                    selected_region = None
                    st.selectbox(
                        "📍 **Region:**",
                        ["Please select zone first"],
                        disabled=True,
                        key="region_disabled"
                    )
            
            # 3. DIVISION Selection (depends on region)
            if zones and selected_region:
                divisions_in_region = zones_data[zones][selected_region]
                selected_division = st.selectbox(
                    "🏢 **Division:**",
                    divisions_in_region,
                    index=None,
                    placeholder="Select division...",
                    key="division_select"
                )
                self.form_data['division'] = selected_division
            
            # 4. Name
            name = st.text_input(
                "👤 **Full Name:**",
                placeholder="Enter full name (e.g., John Smith)",
                key="name_input"
            )
            if name:
                self.form_data['name'] = self.format_name(name)
            
            # 5. Gender
            col3, col4 = st.columns(2)
            
            with col3:
                gender = st.selectbox(
                    "⚥ **Gender:**",
                    ["", "Male", "Female"],
                    index=0,
                    placeholder="Select gender...",
                    key="gender_select"
                )
                self.form_data['gender'] = gender
            
            # 6. Position
            with col4:
                position = st.text_input(
                    "💼 **Position/Title:**",
                    placeholder="Enter position (e.g., Field Officer)",
                    key="position_input"
                )
                if position:
                    self.form_data['position'] = self.format_position(position)
            
            # 7. Contact
            contact = st.text_input(
                "📱 **Contact Number:**",
                placeholder="Enter 10-digit number (e.g., 0241234567)",
                max_chars=10,
                key="contact_input"
            )
            if contact:
                is_valid, message = self.validate_contact(contact)
                if not is_valid:
                    st.error(f"❌ {message}")
                else:
                    self.form_data['contact'] = message
    
    def display_submission_section(self):
        """Display submission button and logic"""
        with st.container(border=True):
            submit_button = st.button(
                    "🚀 **SUBMIT**",
                    type="primary",
                    use_container_width=True
                )
                
            if submit_button:
                    return self.validate_and_submit()
            return False
    
    def validate_and_submit(self):
        """Validate all fields and submit data"""
        required_fields = ['zone', 'region', 'division', 'name', 'gender', 'position', 'contact']
        missing_fields = []
        
        # Check for missing required fields
        for field in required_fields:
            if field not in self.form_data or not self.form_data[field]:
                missing_fields.append(field)
        
        if missing_fields:
            st.error(f"❌ **Missing required fields:** {', '.join(missing_fields).replace('_', ' ').title()}")
            return False
        
        # Validate contact specifically
        if 'contact' in self.form_data:
            is_valid, message = self.validate_contact(self.form_data['contact'])
            if not is_valid:
                st.error(f"❌ Contact validation failed: {message}")
                return False
        
        # If all validations pass, submit to Google Sheets
        return self.submit_to_google_sheets()
    
    def submit_to_google_sheets(self):
        """Submit data to Google Sheets using provided credentials"""
        try:
            # Get all existing data for duplicate checking
            existing_data = self.worksheet.get_all_values()
            
            # Prepare data for submission
            submission_data = [
                str(datetime.now()),
                self.form_data.get('zone', ''),
                self.form_data.get('region', ''),
                self.form_data.get('division', ''),
                self.form_data.get('name', ''),
                self.form_data.get('gender', ''),
                self.form_data.get('position', ''),
                self.form_data.get('contact', '')
            ]
            
            # Convert None values to empty strings for comparison
            submission_data_str = [str(item) if item is not None else "" for item in submission_data]
            
            # Check for duplicate entries
            # Skip the first row (headers) when checking duplicates
            is_duplicate = False
            for row in existing_data[1:]:  # Skip header row
                # Compare key fields: zone, region, division, name, and contact
                row_zone = row[1] if len(row) > 1 else ""
                row_region = row[2] if len(row) > 2 else ""
                row_division = row[3] if len(row) > 3 else ""
                row_name = row[4] if len(row) > 4 else ""
                row_contact = row[7] if len(row) > 7 else ""
                
                # Normalize names for case-insensitive comparison
                submitted_name = self.form_data.get('name', '').lower().strip()
                existing_name = row_name.lower().strip()
                
                if (row_zone == self.form_data.get('zone', '') and
                    row_region == self.form_data.get('region', '') and
                    row_division == self.form_data.get('division', '') and
                    existing_name == submitted_name and
                    row_contact == self.form_data.get('contact', '')):
                    is_duplicate = True
                    break
            
            if is_duplicate:
                st.error("❌ Same entry already exists!")
                return False
            else:
                # Check network connection before appending
                st.success("✅ Network Active!")
                
                # Append to worksheet
                self.worksheet.append_row(submission_data)
                
                # Success message
                st.success("✅ Successfully submitted!")
                st.balloons()
                
                # Reset form
                self.reset_form()
                return True
            
        except Exception as e:
            st.error(f"❌ **Submission failed:** {str(e)}")
            st.info("⚠️ Please check your internet connection and try again.")
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
        """Main method to run the form"""
        self.display_section_a()
        submitted = self.display_submission_section()

def reg():
    """Main function to run the Full-Time Workers Registration form"""
    form = FullTimeWorkersForm()
    form.run()

# Run the application
if __name__ == "__main__":
    reg()