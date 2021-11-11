from flask import Blueprint, request, session, jsonify, make_response
from flask_restful import Api, Resource

from math import ceil

from .db_connect import get_db

bp = Blueprint("search", __name__, url_prefix="/search")
api = Api(bp)

class Search(Resource):
    def get(self):
        q = request.args.get("q", None)
        type = request.args.get("type", 'name')
        page = int(request.args.get("page", 1))

        db = get_db()
        cursor = db.cursor()
        
        # 권한 체크
        username = session.get('username', None)
        if username is None:
            return make_response(jsonify(message='로그인을 해주세요.'), 401)
        else:
            cursor.execute(
                f"SELECT p_search FROM permission WHERE username = {username}"
            )
            perm = cursor.fetchone()
            
            if perm is None or perm['p_search'] == 0:
                return make_response(jsonify(message='검색 권한이 없습니다.'), 403)

        if q is None:
            return jsonify(result=[])
        else:
            limit = 10
            if type == 'name':
                cursor.execute(
                    f"SELECT COUNT(*) AS count FROM center WHERE facilityName LIKE '%{q}%'"
                )
                totalPage = ceil(int(cursor.fetchone()['count']) / 10)
                if totalPage == 0:
                    page = 1
                    totalPage = 1
                elif page >= totalPage:
                    page = totalPage
                
                offset = (page - 1) * limit
                cursor.execute(
                    f"SELECT * FROM center WHERE facilityName LIKE '%{q}%' ORDER BY id LIMIT 10 OFFSET {offset}"
                )
            elif type == 'addr':
                cursor.execute(
                    f"SELECT COUNT(*) AS count FROM center WHERE full_address LIKE '%{q}%'"
                )
                totalCount = cursor.fetchone()
                totalPage = ceil(int(totalCount['count']) / 10)
                if totalPage == 0:
                    page = 1
                    totalPage = 1
                elif page >= totalPage:
                    page = totalPage
                
                offset = (page - 1) * limit
                cursor.execute(
                    f"SELECT * FROM center WHERE full_address LIKE '%{q}%' ORDER BY id LIMIT 10 OFFSET {offset}"
                )
            result = cursor.fetchall()
        
        return jsonify(result=result, totalPage=totalPage)

api.add_resource(Search, '/center')