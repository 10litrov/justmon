from twisted.application.service import ServiceMaker


justmon = ServiceMaker('justmon', 'justmon.tap', 'A simple host monitoring service.', 'justmon')
