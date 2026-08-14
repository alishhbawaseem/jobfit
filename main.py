"""
JobFit - Phase 1: Command-line test
Resume aur job description do, match analysis + cover letter terminal pe dekho.
"""

from resume_agent import load_resume_text, build_vector_store, analyze_fit, generate_cover_letter


def main():
    print("=== JobFit: AI Job Matching Agent ===\n")

    resume_path = input("Resume ka path do (PDF ya .txt): ").strip()

    print("\nResume padh rahe hain aur chunks bana rahe hain...")
    resume_text = load_resume_text(resume_path)
    vector_store = build_vector_store(resume_text)
    print(f"Resume ke {len(resume_text)} characters process ho gaye.\n")

    print("Job description paste karo (khatam karne ke liye ek khali line pe Enter dabao):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    job_description = "\n".join(lines)

    print("\nAnalyze kar rahe hain...\n")
    result = analyze_fit(vector_store, job_description)

    print("--- Match Analysis ---")
    print(f"Match Score: {result['match_score']}/100")
    print(f"Matching Skills: {', '.join(result['matching_skills'])}")
    print(f"Missing Skills: {', '.join(result['missing_skills'])}")
    print(f"Summary: {result['summary']}")

    make_letter = input("\nCover letter bhi banayein? (y/n): ").strip().lower()
    if make_letter == "y":
        print("\nCover letter likh rahe hain...\n")
        letter = generate_cover_letter(vector_store, job_description)
        print("--- Cover Letter ---")
        print(letter)


if __name__ == "__main__":
    main()