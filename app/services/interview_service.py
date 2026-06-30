from fastapi import Depends

from app.agents.interview_agent import InterviewAgent, get_interview_agent
from app.model.requests.interview import InterviewRequest, InterviewResponse


class InterviewService:
	def __init__(self, interview_agent: InterviewAgent) -> None:
		self.interview_agent = interview_agent

	def process(self, payload: InterviewRequest) -> InterviewResponse:
		return self.interview_agent.answer(payload)


def get_interview_service(
	interview_agent: InterviewAgent = Depends(get_interview_agent),
) -> InterviewService:
	return InterviewService(interview_agent)
