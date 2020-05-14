from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect


global records, number_of_ticket
records = []
number_of_ticket = None


def find_next_ticket():
    oil_list = [item for item in records if item["type"] == 1]
    tir_list = [item for item in records if item["type"] == 2]
    dia_list = [item for item in records if item["type"] == 3]

    # Firstly change_oil
    if oil_list:
        return oil_list[0]

    # Then inflate_tires
    elif tir_list:
        return tir_list[0]

    # And only then diagnostic
    elif dia_list:
        return dia_list[0]

    return None


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html')


class NextPageView(View):
    def get(self, request, *args, **kwargs):
        # next_ticket = find_next_ticket()
        # number_of_ticket = next_ticket['index'] if next_ticket else None
        return render(request, 'tickets/next.html', context={'number_of_ticket': number_of_ticket})


class GetTicketView(View):

    def get(self, request, *args, **kwargs):
        services = {'change_oil': 1, 'inflate_tires': 2, 'diagnostic': 3}
        current_ticket = services[request.path.split("/")[-2]]

        # Changing oil
        oil_list = [item for item in records if item["type"] == 1]
        queue_number = len(oil_list)
        estimated_time = len(oil_list) * 2

        # inflate tires
        if current_ticket > 1:
            tir_list = [item for item in records if item["type"] == 2]
            queue_number += len(tir_list)
            estimated_time += len(tir_list) * 5

        # diagnostic
        if current_ticket > 2:
            dia_list = [item for item in records if item["type"] == 3]
            queue_number += len(dia_list)
            estimated_time += len(dia_list) * 30

        index = len(records) + 1
        records.append({"index": index, "type": current_ticket})

        return render(request, 'tickets/get_ticket.html',
                      context={'queue_number': queue_number, 'estimated_time': estimated_time})


class OperatorView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/processing.html',
                      context={'oil_q': len([item for item in records if item["type"] == 1]),
                               'tir_q': len([item for item in records if item["type"] == 2]),
                               'dia_q': len([item for item in records if item["type"] == 3])})


    def post(self, *args, **kwargs):
        next_ticket = find_next_ticket()
        if next_ticket:
            records.remove(next_ticket)
            global number_of_ticket
            number_of_ticket = next_ticket['index']
        else:
            number_of_ticket = None
        return redirect('/next')
