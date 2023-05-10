import excel_parser
import db_handler


def lambda_handler(event, _context):

    # s3에 저장된 excel 파일 위치 정보 추출
    # bucket_name = event['Records'][0]['s3']['bucket']['name']
    # file_name = event['Records'][0]['s3']['object']['key']

    # 로컬에 저장된 excel 파일 경로
    bucket_name = None
    file_name = event

    # 확장자 및 시트 명 추출
    extension, names = excel_parser.extract_file_name(file_name)

    # excel 파일 읽기
    data = excel_parser.read_data(bucket_name, file_name, extension)

    # excel 데이터 전처리
    data = excel_parser.preprocess_data(data)

    # excel 데이터 파싱
    data = excel_parser.parse_data(names, data)

    # DB 접근
    db_handler.connect_db(data)


if __name__ == '__main__':
    event = ''
    _context = ''
    lambda_handler(event, _context)
