from django.shortcuts import render
from exceptions import InvalidYearCupError
from exceptions import NegativeTitlesError
from exceptions import ImpossibleTitlesError
from rest_framework.views import APIView, Response, Request, status
from django.forms.models import model_to_dict
from utils import data_processing
from .models import Team

# Create your views here.

class TeamView(APIView):
    def get(self, request: Request) -> Response:
        teams = Team.objects.all()

        team_list = []
        for team in teams:
            team_dict = model_to_dict(team)
            team_list.append(team_dict)

        return Response(team_list, status.HTTP_200_OK)
    
    def post(self, request: Request) -> Response:
        try:
            data_processing(request.data)
        except NegativeTitlesError as error:
            return Response({'error': error.message}, status.HTTP_400_BAD_REQUEST)
        
        except InvalidYearCupError as error:
            return Response({'error': error.message}, status.HTTP_400_BAD_REQUEST)
        
        except ImpossibleTitlesError as error:
            return Response({'error': error.message}, status.HTTP_400_BAD_REQUEST)
        
        team = Team.objects.create(**request.data)
        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_201_CREATED)
    
class TeamDetailView(APIView):
    def get(self, request: Request, team_id:int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)
        
        team_dict = model_to_dict(team)
        return Response(team_dict, status.HTTP_200_OK)
    
    def patch(self, request: Request, team_id:int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)
        
        for key, value in request.data.items():
            setattr(team, key, value)

        team.save()
        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_200_OK)
    
    def delete(self, request: Request, team_id:int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)
        
        team.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
        
            