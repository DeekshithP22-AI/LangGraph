# import requests
# import json
# import time
# import os
# from urllib.parse import urljoin
# import uuid

# class ReportDownloader:
#     def __init__(self, email):
#         self.base_url = "https://thevcproject.in"
#         self.session = requests.Session()
#         self.guest_id = f"guest_{int(time.time()*1000)}_{uuid.uuid4().hex[:8]}"
#         self.email = email
        
#     def register_email(self):
#         """Register email with the site"""
#         url = urljoin(self.base_url, "/api/check-email")
#         params = {
#             "guestId": self.guest_id,
#             "email": self.email
#         }
#         try:
#             response = self.session.get(url, params=params)
#             response.raise_for_status()
#             return response.json()
#         except requests.exceptions.RequestException as e:
#             print(f"Error registering email: {e}")
#             return None

#     def subscribe_to_report(self, report_id):
#         """Subscribe to a specific report"""
#         url = urljoin(self.base_url, "/api/report-subscribe")
#         data = {
#             "guestId": self.guest_id,
#             "email": self.email,
#             "reportId": report_id
#         }
#         try:
#             response = self.session.post(url, json=data)
#             response.raise_for_status()
#             return response.json()
#         except requests.exceptions.RequestException as e:
#             print(f"Error subscribing to report: {e}")
#             return None

#     def get_reports_list(self):
#         """Get list of available reports"""
#         url = urljoin(self.base_url, "/api/reports")
#         try:
#             response = self.session.get(url)
#             response.raise_for_status()
#             data = response.json()
#             return data.get('reports', [])
#         except requests.exceptions.RequestException as e:
#             print(f"Error getting reports list: {e}")
#             return None
#         except json.JSONDecodeError as e:
#             print(f"Error parsing JSON response: {e}")
#             return None

#     def download_report(self, report_url, filename):
#         """Download a report from direct URL"""
#         try:
#             response = self.session.get(report_url, stream=True)
#             response.raise_for_status()
            
#             with open(filename, 'wb') as f:
#                 for chunk in response.iter_content(chunk_size=8192):
#                     if chunk:
#                         f.write(chunk)
#             return True
#         except requests.exceptions.RequestException as e:
#             print(f"Error downloading report: {e}")
#             return False

#     def download_all_reports(self, output_dir=None):
#         """Download all available reports"""
#         # Set default output directory to current directory if none specified
#         if output_dir is None:
#             output_dir = os.path.join(os.getcwd(), "downloaded_reports")
        
#         # Create output directory if it doesn't exist
#         os.makedirs(output_dir, exist_ok=True)
#         print(f"Reports will be saved to: {output_dir}")
        
#         # Register email
#         print(f"Registering email: {self.email}")
#         self.register_email()
        
#         # Get list of reports
#         reports = self.get_reports_list()
#         if not reports:
#             print("No reports found. Exiting...")
#             return
        
#         print(f"Found {len(reports)} reports to download.")
        
#         for report in reports:
#             try:
#                 # Extract report details
#                 title = report['title']
#                 report_id = report['rid']
#                 pdf_url = report['link']
                
#                 # Clean filename
#                 safe_title = "".join(x for x in title if x.isalnum() or x in (' ', '-', '_')).rstrip()
#                 filename = os.path.join(output_dir, f"{safe_title}.pdf")
                
#                 # Subscribe to report
#                 print(f"\nProcessing: {title}")
#                 self.subscribe_to_report(report_id)
                
#                 # Download the report
#                 print(f"Downloading to: {filename}")
#                 success = self.download_report(pdf_url, filename)
                
#                 if success:
#                     print(f"Successfully downloaded: {title}")
#                 else:
#                     print(f"Failed to download: {title}")
                
#                 # Add a small delay between downloads
#                 time.sleep(1)
                
#             except Exception as e:
#                 print(f"Error processing report {report.get('title', 'Unknown')}: {e}")
#                 continue

# def main():
#     # Specify the output directory (optional)
#     output_dir = os.path.join(os.getcwd(), "downloaded_reports")
    
#     email = input("Please enter your email address: ")
#     downloader = ReportDownloader(email)
#     downloader.download_all_reports(output_dir)
#     print(f"\nDownload complete! Check the files in: {output_dir}")

# if __name__ == "__main__":
#     main()


import requests
import json
import time
import os
from urllib.parse import urljoin
import uuid

class ReportDownloader:
    def __init__(self, email):
        self.base_url = "https://thevcproject.in"
        self.session = requests.Session()
        self.guest_id = f"guest_{int(time.time()*1000)}_{uuid.uuid4().hex[:8]}"
        self.email = email

    def register_email(self):
        """Register email with the site"""
        url = urljoin(self.base_url, "/api/check-email")
        params = {
            "guestId": self.guest_id,
            "email": self.email
        }
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error registering email: {e}")
            return None

    def subscribe_to_report(self, report_id):
        """Subscribe to a specific report"""
        url = urljoin(self.base_url, "/api/report-subscribe")
        data = {
            "guestId": self.guest_id,
            "email": self.email,
            "reportId": report_id
        }
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error subscribing to report: {e}")
            return None

    # def get_reports_list(self):
    #     """Get list of available reports, including handling Load More functionality"""
    #     url = urljoin(self.base_url, "/api/reports")
    #     all_reports = []
    #     page = 1  # Start with the first page
    #     has_more = True

    #     while has_more:
    #         try:
    #             # Fetch reports for the current page
    #             params = {"page": page}  # Page number for pagination
    #             response = self.session.get(url, params=params)
    #             response.raise_for_status()
    #             data = response.json()

    #             # Extract reports and check if there are additional pages
    #             reports = data.get('reports', [])
    #             all_reports.extend(reports)

    #             # Check if there are more pages
    #             has_more = data.get('hasMore', False)  # Ensure `hasMore` exists in the API response
    #             print(f"Fetched page {page}, {len(reports)} reports found.")

    #             # Increment to the next page
    #             page += 1
    #             time.sleep(1)  # Add delay to avoid overwhelming the server

    #         except requests.exceptions.RequestException as e:
    #             print(f"Error getting reports list on page {page}: {e}")
    #             break
    #         except json.JSONDecodeError as e:
    #             print(f"Error parsing JSON response: {e}")
    #             break

    #     return all_reports
    
    
    def get_reports_list(self):
        """Get the list of all available reports by handling Load More functionality."""
        url = urljoin(self.base_url, "/api/reports")
        all_reports = []
        page = 1  # Start with the first page

        while True:
            try:
                # Fetch the reports for the current page
                params = {"page": page}
                response = self.session.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                # Extract reports
                reports = data.get("reports", [])
                if not reports:
                    # If no reports are returned, we've exhausted all pages
                    print(f"No more reports found on page {page}. Stopping pagination.")
                    break

                all_reports.extend(reports)
                print(f"Fetched page {page}, {len(reports)} reports found.")

                # Increment the page number to fetch the next batch
                page += 1
                time.sleep(1)  # Delay to avoid overwhelming the server

            except requests.exceptions.RequestException as e:
                print(f"Error getting reports list on page {page}: {e}")
                break
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON response on page {page}: {e}")
                break

        return all_reports
    
    

    def download_report(self, report_url, filename):
        """Download a report from direct URL"""
        try:
            response = self.session.get(report_url, stream=True)
            response.raise_for_status()

            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error downloading report: {e}")
            return False

    def download_all_reports(self, output_dir=None):
        """Download all available reports"""
        if output_dir is None:
            output_dir = os.path.join(os.getcwd(), "downloaded_reports")

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        print(f"Reports will be saved to: {output_dir}")

        # Register email
        print(f"Registering email: {self.email}")
        self.register_email()

        # Get list of reports
        reports = self.get_reports_list()
        if not reports:
            print("No reports found. Exiting...")
            return

        print(f"Found {len(reports)} reports to download.")

        for report in reports:
            try:
                # Extract report details
                title = report['title']
                report_id = report['rid']
                pdf_url = report['link']

                # Clean filename
                safe_title = "".join(x for x in title if x.isalnum() or x in (' ', '-', '_')).rstrip()
                filename = os.path.join(output_dir, f"{safe_title}.pdf")

                # Subscribe to the report
                print(f"\nProcessing: {title}")
                self.subscribe_to_report(report_id)

                # Download the report
                print(f"Downloading to: {filename}")
                success = self.download_report(pdf_url, filename)

                if success:
                    print(f"Successfully downloaded: {title}")
                else:
                    print(f"Failed to download: {title}")

                # Add a small delay between downloads
                time.sleep(1)

            except Exception as e:
                print(f"Error processing report {report.get('title', 'Unknown')}: {e}")
                continue

def main():
    # Specify the output directory (optional)
    output_dir = os.path.join(os.getcwd(), "downloaded_reports")

    email = input("Please enter your email address: ")
    downloader = ReportDownloader(email)
    downloader.download_all_reports(output_dir)
    print(f"\nDownload complete! Check the files in: {output_dir}")

if __name__ == "__main__":
    main()